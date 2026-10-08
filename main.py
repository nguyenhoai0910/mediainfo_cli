import sys

import mediainfo_tool
from models import OutputMode
from backends import diff
from tools import check_all

USAGE_MAIN = "Usage: mediainfo -vt|-pt|-pqt <file> [file2 ...]"
USAGE_DIFF = "Usage: mediainfo -diff <file1> <file2>"


def check_deps():
    missing = check_all()
    if missing:
        print("Missing required tools:")
        for msg in missing:
            print(f"  - {msg}")
        sys.exit(1)


def print_help():
    print(USAGE_MAIN)
    print("       mediainfo -diff <file1> <file2>")
    print("  -vt   video template")
    print("  -pt   photo template")
    print("  -pqt  photo quality template")
    print("  -diff compare 2 images")


def main():
    check_deps()

    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    mode_arg = sys.argv[1].lower()

    # ---- diff mode ----
    if mode_arg == '-diff':
        if len(sys.argv) < 4:
            print(USAGE_DIFF)
            sys.exit(1)
        try:
            data = diff.compare(sys.argv[2], sys.argv[3])
            print(diff.format_diff(data))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        return

    # ---- template modes ----
    mode_map = {
        '-vt': OutputMode.VT,
        '-pt': OutputMode.PT,
        '-pqt': OutputMode.PQT,
    }

    if mode_arg not in mode_map:
        print(f"Unknown mode: {mode_arg}")
        print("Valid modes: -vt, -pt, -pqt, -diff")
        sys.exit(1)

    if len(sys.argv) < 3:
        print(USAGE_MAIN)
        sys.exit(1)

    mode = mode_map[mode_arg]
    paths = sys.argv[2:]  # accept multiple files
    had_error = False

    for path in paths:
        print(f"{'=' * 70} {path}")
        try:
            result = mediainfo_tool.read(path, mode)
            print(result)
        except Exception as e:
            # one bad file should not stop the rest
            print(f"Error: {e}")
            had_error = True

    if had_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
