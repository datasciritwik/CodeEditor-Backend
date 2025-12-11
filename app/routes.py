from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from .models import CodeSubmission, CodeExecutionResult
from .executor.sandbox import execute_in_sandbox

router = APIRouter()

@router.post(
    "/questions/{question_id}/run",
    response_model=CodeExecutionResult,
)
async def run_code(
    question_id: str,
    payload: CodeSubmission,
):
    """
    Executes code securely in a sandbox.
    """

    result = execute_in_sandbox(code=payload.code, language=payload.language)
    return JSONResponse(
        content={"results":result, "questionId": question_id},
        status_code=status.HTTP_200_OK
    )