import os
import shutil
import subprocess
import sys

INSTALL_HINT = {
    'ffprobe':  'sudo apt install ffmpeg',
    'exiftool': 'sudo apt install libimage-exiftool-perl',
    'magick':   'sudo apt install imagemagick',
}


def find_tool(name: str) -> str:
    # 1. Look for a bundled copy in the bin folder (mainly for Windows builds)
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    local = os.path.join(base, 'bin', name + ('.exe' if os.name == 'nt' else ''))
    if os.path.isfile(local):
        return local

    # 2. Fall back to the system PATH
    path = shutil.which(name)
    if path:
        return path

    hint = INSTALL_HINT.get(name, '')
    raise RuntimeError(f"'{name}' is not installed. Install it with: {hint}")


def check_all() -> list:
    """Call at startup. Returns a list of error messages for missing tools."""
    missing = []
    for name in INSTALL_HINT:
        try:
            find_tool(name)
        except RuntimeError as e:
            missing.append(str(e))
    return missing


def clean_env() -> dict:
    """Environment for child processes, without PyInstaller's library path."""
    env = os.environ.copy()
    for var in ('LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH'):
        orig = env.get(var + '_ORIG')
        if orig is not None:
            env[var] = orig      # restore the user's original value
        else:
            env.pop(var, None)   # it was not set before, so remove it
    return env


def run(cmd: list) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=clean_env())
    except FileNotFoundError:
        raise RuntimeError(f"Cannot run '{cmd[0]}': file not found")
    except PermissionError:
        raise RuntimeError(f"Cannot run '{cmd[0]}': permission denied (try: chmod +x)")
    except OSError as e:
        raise RuntimeError(f"Cannot run '{cmd[0]}': {e}")

    if result.returncode != 0:
        name = os.path.basename(cmd[0])
        err = result.stderr.strip() or 'no error message'
        raise RuntimeError(f"'{name}' failed (exit code {result.returncode}): {err}")

    return result