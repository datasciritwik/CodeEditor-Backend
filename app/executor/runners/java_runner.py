import subprocess, os, re
from app.utils.file_utils import sanitize_filename, temporary_workdir

def run(code: str, work_dir: str, file_id:str):
    # Extract class name from Java code
    match = re.search(r'public\s+class\s+(\w+)', code)
    if not match:
        return "", "Error: Could not find public class declaration in Java code"
    
    class_name = match.group(1)
    safe_class_name = sanitize_filename(class_name)
    
    # Create file with class name
    file_path = os.path.join(work_dir, f"{safe_class_name}.java")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")

    compile_proc = subprocess.run(
        ["javac", file_path],
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
