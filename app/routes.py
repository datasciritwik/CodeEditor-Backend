from fastapi import APIRouter, Header, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from .models import CodeSubmission, CodeExecutionResult
from .executor.sandbox import execute_in_sandbox
from .utils.fernet_utils import verify_fernet_token
# Load key from environment or raise error
router = APIRouter()

# Define the security scheme for Swagger UI
api_key_header = APIKeyHeader(name="authorization", auto_error=False)

@router.post(
    "/questions/{question_id}/run",
    response_model=CodeExecutionResult,
)
async def run_code(
    question_id: str,
    payload: CodeSubmission,
    authorization: str = Depends(api_key_header),
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
    return JSONResponse(
        content={"results":result, "questionId": question_id},
        status_code=status.HTTP_200_OK
    )