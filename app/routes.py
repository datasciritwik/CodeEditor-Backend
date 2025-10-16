from fastapi import APIRouter, Header, HTTPException, status
from .models import CodeSubmission, CodeExecutionResult
from .executor.sandbox import execute_in_sandbox
from .utils.fernet_utils import verify_fernet_token

router = APIRouter()

@router.post(
    "/questions/{question_id}/run",
    response_model=CodeExecutionResult,
)
async def run_code(
    question_id: str,
    payload: CodeSubmission,
    authorization: str = Header(None, description="Fernet token for secure access"),
):
    """
    Executes code securely in a sandbox.
    Access protected via Fernet token.
    """
    if not authorization or not verify_fernet_token(authorization):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authorization token."
        )

    result = execute_in_sandbox(code=payload.code, language=payload.language)
    return result
