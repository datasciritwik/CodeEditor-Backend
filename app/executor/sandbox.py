import time
from app.utils.file_utils import temporary_workdir
from .runners import python_runner, cpp_runner, c_runner, java_runner, js_runner

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
            exec_time = int((time.time() - start) * 1000)
            return {"stdout": stdout, "stderr": stderr, "execution_time_ms": exec_time, "was_successful": stderr == ""}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "execution_time_ms": 0, "was_successful": False}
