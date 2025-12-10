"""FastAPI routes for patent litigation report generation."""

import uuid
from typing import Any

import structlog
from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from src.patent_pipeline.models.requests import (
    GenerateReportRequest,
    GenerateReportResponse,
    PipelineStatusResponse,
)
from src.patent_pipeline.graph import run_patent_pipeline
from src.patent_pipeline.state import PatentPipelineState

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/patent-reports", tags=["Patent Reports"])

# In-memory job storage (use Redis in production)
_jobs: dict[str, dict[str, Any]] = {}


@router.post(
    "/generate",
    response_model=GenerateReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Patent Litigation Reports",
    description="""
    Generate litigation-ready reports from patent and prosecution history PDFs.

    This endpoint processes the provided PDFs through a multi-stage pipeline:
    1. Stage 1: Record Extraction
    2. Stage 2A-C: Analysis (Claim Construction, Search/Technical, Timeline)
    3. Stage 3: Report Generation
    4. Stage 4: QC & Verification
    5. Search Intelligence (Pipeline 2 sidecar)

    The generated reports are saved to the same Azure container as the input PDFs.

    **Note:** This is a synchronous endpoint that blocks until processing completes.
    For large documents, consider using the async endpoint instead.
    """,
)
def generate_reports(request: GenerateReportRequest) -> GenerateReportResponse:
    """Generate patent litigation reports synchronously.

    Args:
        request: Request containing patent and history PDF URLs

    Returns:
        Response containing URLs to generated reports

    Raises:
        HTTPException: If pipeline fails
    """
    logger.info(
        "Received report generation request",
        patent_url=request.patent_pdf_url[:50] + "...",
        history_url=request.history_pdf_url[:50] + "...",
    )

    try:
        # Run the pipeline
        result = run_patent_pipeline(
            patent_pdf_url=request.patent_pdf_url,
            history_pdf_url=request.history_pdf_url,
        )

        # Check for failure
        if result.get("status") == "failed":
            error_msg = result.get("error", "Unknown pipeline error")
            logger.error("Pipeline failed", error=error_msg)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Pipeline failed: {error_msg}",
            )

        # Extract QC score if available
        qc_score = None
        qc_json = result.get("stage4_qc_json")
        if qc_json and "metrics" in qc_json:
            qc_score = qc_json["metrics"].get("overall_quality_score")

        response = GenerateReportResponse(
            stage3_url=result.get("stage3_url", ""),
            stage4_url=result.get("stage4_url", ""),
            search_intel_url=result.get("search_intel_url"),
            pipeline_status=result.get("status", "completed"),
            qc_score=qc_score,
        )

        logger.info(
            "Report generation completed",
            stage3_url=response.stage3_url,
            stage4_url=response.stage4_url,
            qc_score=qc_score,
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error during report generation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router.post(
    "/generate/async",
    response_model=PipelineStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate Patent Litigation Reports (Async)",
    description="""
    Start asynchronous generation of litigation-ready reports.

    Returns immediately with a job ID that can be used to check status.
    Use the /status/{job_id} endpoint to poll for completion.
    """,
)
async def generate_reports_async(
    request: GenerateReportRequest,
    background_tasks: BackgroundTasks,
) -> PipelineStatusResponse:
    """Generate patent litigation reports asynchronously.

    Args:
        request: Request containing patent and history PDF URLs
        background_tasks: FastAPI background tasks

    Returns:
        Response containing job ID for status polling
    """
    job_id = str(uuid.uuid4())

    logger.info(
        "Starting async report generation",
        job_id=job_id,
        patent_url=request.patent_pdf_url[:50] + "...",
        history_url=request.history_pdf_url[:50] + "...",
    )

    # Initialize job status
    _jobs[job_id] = {
        "status": "pending",
        "current_stage": "queued",
        "progress_percent": 0.0,
        "result": None,
        "error_message": None,
    }

    # Add background task
    background_tasks.add_task(
        _run_pipeline_background,
        job_id,
        request.patent_pdf_url,
        request.history_pdf_url,
    )

    return PipelineStatusResponse(
        job_id=job_id,
        status="pending",
        current_stage="queued",
        progress_percent=0.0,
    )


@router.get(
    "/status/{job_id}",
    response_model=PipelineStatusResponse,
    summary="Get Pipeline Status",
    description="Get the status of an asynchronous report generation job.",
)
def get_pipeline_status(job_id: str) -> PipelineStatusResponse:
    """Get status of an async pipeline job.

    Args:
        job_id: Job identifier from async generation

    Returns:
        Current status of the job

    Raises:
        HTTPException: If job not found
    """
    if job_id not in _jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job not found: {job_id}",
        )

    job = _jobs[job_id]

    result = None
    if job["result"]:
        result = GenerateReportResponse(
            stage3_url=job["result"].get("stage3_url", ""),
            stage4_url=job["result"].get("stage4_url", ""),
            search_intel_url=job["result"].get("search_intel_url"),
            pipeline_status=job["result"].get("status", "completed"),
        )

    return PipelineStatusResponse(
        job_id=job_id,
        status=job["status"],
        current_stage=job["current_stage"],
        progress_percent=job["progress_percent"],
        error_message=job["error_message"],
        result=result,
    )


async def _run_pipeline_background(
    job_id: str,
    patent_pdf_url: str,
    history_pdf_url: str,
) -> None:
    """Run pipeline in background task.

    Args:
        job_id: Job identifier
        patent_pdf_url: URL to patent PDF
        history_pdf_url: URL to history PDF
    """
    logger.info("Background pipeline started", job_id=job_id)

    try:
        _jobs[job_id]["status"] = "processing"
        _jobs[job_id]["current_stage"] = "ingest_pdfs"
        _jobs[job_id]["progress_percent"] = 5.0

        # Run the pipeline
        result = run_patent_pipeline(
            patent_pdf_url=patent_pdf_url,
            history_pdf_url=history_pdf_url,
        )

        if result.get("status") == "failed":
            _jobs[job_id]["status"] = "failed"
            _jobs[job_id]["error_message"] = result.get("error", "Unknown error")
            _jobs[job_id]["progress_percent"] = 100.0
        else:
            _jobs[job_id]["status"] = "completed"
            _jobs[job_id]["current_stage"] = "completed"
            _jobs[job_id]["progress_percent"] = 100.0
            _jobs[job_id]["result"] = {
                "stage3_url": result.get("stage3_url"),
                "stage4_url": result.get("stage4_url"),
                "search_intel_url": result.get("search_intel_url"),
                "status": "completed",
            }

        logger.info(
            "Background pipeline completed",
            job_id=job_id,
            status=_jobs[job_id]["status"],
        )

    except Exception as e:
        logger.exception("Background pipeline failed", job_id=job_id)
        _jobs[job_id]["status"] = "failed"
        _jobs[job_id]["error_message"] = str(e)
        _jobs[job_id]["progress_percent"] = 100.0
