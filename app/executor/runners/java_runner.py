import subprocess, os
from app.utils.file_utils import create_temp_source_file

def run(code: str, work_dir: str, file_id: str):
    # Use class name matching file_id
    src = create_temp_source_file(code, "java", work_dir)
    class_name = os.path.splitext(os.path.basename(src))[0]

    compile_proc = subprocess.run(
        ["javac", src],
        capture_output=True,
        text=True,
    )
    if compile_proc.returncode != 0:
        return "", compile_proc.stderr

    run_proc = subprocess.run(
        ["java", "-cp", work_dir, class_name],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return run_proc.stdout, run_proc.stderr
