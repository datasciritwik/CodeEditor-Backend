import subprocess
from app.utils.file_utils import create_temp_source_file

def run(code: str, work_dir: str, file_id: str):
    file_path = create_temp_source_file(code, "py", work_dir)
    result = subprocess.run(
        ["python3", file_path],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout, result.stderr
