import subprocess, os
from app.utils.file_utils import create_temp_source_file

def run(code: str, work_dir: str, file_id: str):
    src = create_temp_source_file(code, "cpp", work_dir)
    binary = os.path.join(work_dir, f"{file_id}.out")

    compile_proc = subprocess.run(
        ["g++", src, "-o", binary],
        capture_output=True,
        text=True,
    )
    if compile_proc.returncode != 0:
        return "", compile_proc.stderr

    run_proc = subprocess.run(
        [binary],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return run_proc.stdout, run_proc.stderr
