import mediainfo_tool
from models import OutputMode
from backends import diff
import shutil, sys

REQUIRED = ['exiftool', 'ffprobe', 'magick', 'sha256sum']

def check_deps():
    missing = [t for t in REQUIRED if not shutil.which(t)]
    if missing:
        print(f"Missing tools: {', '.join(missing)}")
        print("Install with: sudo apt install ffmpeg imagemagick libimage-exiftool-perl")
        sys.exit(1)

def main():
    check_deps()

    if len(sys.argv) < 2:
        print("Usage: mediainfo -vt|-pt|-pqt <file> [file2 ...]")
        print("       mediainfo -diff <file1> <file2>")
        print("  -vt   video template")
        print("  -pt   photo template")
        print("  -pqt  photo quality template")
        print("  -diff compare 2 images")
        sys.exit(1)

    mode_arg = sys.argv[1].lower()

    if mode_arg == '-diff':
        if len(sys.argv) < 4:
            print("Usage: mediainfo -diff <file1> <file2>")
            sys.exit(1)
        path1 = sys.argv[2]
        path2 = sys.argv[3]
        data = diff.compare(path1, path2)
        print(diff.format_diff(data))
        return

    if len(sys.argv) < 3:
        print("Usage: mediainfo -vt|-pt|-pqt <file> [file2 ...]")
        sys.exit(1)

    mode_map = {
        '-vt': OutputMode.VT,
        '-pt': OutputMode.PT,
        '-pqt': OutputMode.PQT,
    }

    if mode_arg not in mode_map:
        print(f"Unknown mode: {mode_arg}")
        print("Valid modes: -vt, -pt, -pqt, -diff")
        sys.exit(1)

    mode = mode_map[mode_arg]
    paths = sys.argv[2:]  # nhận nhiều file

    for path in paths:
        print(f"{'=' * 70} {path}")
        result = mediainfo_tool.read(path, mode)
        print(result)

if __name__ == "__main__":
    main()
