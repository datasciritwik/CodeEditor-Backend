import time
import re
from app.utils.file_utils import temporary_workdir
from .runners import python_runner, cpp_runner, c_runner, java_runner, js_runner

def clean_error_message(stderr: str, ) -> str:
    """
    Removes temporary file paths from error messages to show only relevant errors.
    """
    if not stderr:
        return stderr
    
    # Remove full file paths, keep only "line X" info
    stderr = re.sub(r'File "[^"]*[/\\]([^/\\]+\.py)"', r'File "\1"', stderr)
    stderr = re.sub(r'File "[^"]*[/\\]([^/\\]+\.java)"', r'File "\1"', stderr)
    stderr = re.sub(r'File "[^"]*[/\\]([^/\\]+\.js)"', r'File "\1"', stderr)
    stderr = re.sub(r'File "[^"]*[/\\]([^/\\]+\.(c|cpp))"', r'File "\1"', stderr)
    
    # Remove UUID-based filenames, replace with generic "main"
    stderr = re.sub(r'File "[\w-]{36}\.(py|java|js|c|cpp)"', r'File "main.\1"', stderr)
    
    # For C/C++ errors with file paths
    stderr = re.sub(r'/tmp/[^:]+:', '', stderr)
    
    return stderr.strip()

def execute_in_sandbox(code: str, language: str):
    """Executes code securely in a disposable sandbox directory."""
    start = time.time()

    runners = {
        "python": python_runner,
        "cpp": cpp_runner,
        "c": c_runner,
        "java": java_runner,
        "javascript": js_runner,
        "js": js_runner
    }

    runner = runners.get(language.lower())
    if not runner:
        return {"stdout": "", "stderr": f"Unsupported language: {language}", "execution_time_ms": 0, "was_successful": False}

    with temporary_workdir() as tmp_dir:
        try:
            stdout, stderr = runner.run(code, tmp_dir, "main")
            
            # Clean up error messages
            stderr = clean_error_message(stderr)
            
            exec_time = int((time.time() - start) * 1000)
            return {"stdout": stdout, "stderr": stderr, "execution_time_ms": exec_time, "was_successful": stderr == ""}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "execution_time_ms": 0, "was_successful": False}