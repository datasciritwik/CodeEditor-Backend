import os
import tempfile
import uuid
import shutil
import re
from contextlib import contextmanager

def sanitize_filename(filename: str) -> str:
    """
    Removes unsafe characters from filenames.
    Prevents directory traversal or shell injection.
    """
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)
    return filename[:64]  # limit length

@contextmanager
def temporary_workdir(prefix: str = "sandbox_"):
    """
    Creates a temporary directory for code execution and auto-cleans it up.
    Usage:
        with temporary_workdir() as workdir:
            # do work inside
    """
    tmp_dir = tempfile.mkdtemp(prefix=prefix)
    try:
        yield tmp_dir
    finally:
        try:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception:
            pass

def create_temp_source_file(code: str, extension: str, workdir: str) -> str:
    """
    Creates a temporary source file with a unique ID inside the given workdir.
    Returns the full file path.
    """
    unique_id = str(uuid.uuid4())
    filename = sanitize_filename(f"{unique_id}.{extension}")
    filepath = os.path.join(workdir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")

    return filepath
