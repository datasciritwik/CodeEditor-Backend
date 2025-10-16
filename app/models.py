from pydantic import BaseModel, Field

class CodeSubmission(BaseModel):
    code: str = Field(..., description="User-submitted code")
    language: str = Field(..., example="python", description="Language identifier")

class CodeExecutionResult(BaseModel):
    stdout: str
    stderr: str
    execution_time_ms: int
    was_successful: bool
