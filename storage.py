"""Reading and writing the todo file."""

import json
import os
import tempfile
from pathlib import Path


def load(path):
    path = Path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _mode_for(path):
    try:
        return os.stat(path).st_mode & 0o7777
    except FileNotFoundError:
        umask = os.umask(0)
        os.umask(umask)
        return 0o666 & ~umask


def save(path, items):
    path = Path(os.path.realpath(path))
    data = (json.dumps(items, indent=2) + "\n").encode("utf-8")
    mode = _mode_for(path)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as file:
            file.write(data)
            file.flush()
            os.fsync(file.fileno())
        os.chmod(temp, mode)
        os.replace(temp, path)
    except BaseException:
        try:
            os.unlink(temp)
        except FileNotFoundError:
            pass
        raise
