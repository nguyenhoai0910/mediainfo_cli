# Custom MediaInfo Tool

A replacement for the original `mediainfo` binary, using more accurate and specialized backends to extract metadata from images and videos, with additional quality analysis and image comparison features.

---

## Why Not Use Original mediainfo

- Known bug where it misreads file size and confuses filenames between files in the same directory
- No image quality analysis (brightness, contrast, verdict)
- No diff/comparison mode

---

## Backends

| Tool | Purpose |
|------|---------|
| `exiftool` | Reads image metadata (width, height, bit depth, comment) |
| `ffprobe` | Reads video metadata (codec, fps, bitrate, duration) |
| `magick` (ImageMagick) | Analyzes image quality (brightness, contrast, balance, verdict) |
| Binary header reader | Accurately determines Lossy/Lossless compression without guessing by file extension |
| `sha256sum` | File integrity hash |

---

## Modes

| Flag | Description |
|------|-------------|
| `-pt` | Basic image info |
| `-pqt` | Image info + quality analysis |
| `-vt` | Video info |
| `-diff` | Pixel-level comparison between 2 images, returns similarity score |

---

## Usage

```bash
# single file
mediainfo -pt image.jpg
mediainfo -pqt image.png
mediainfo -vt video.mp4

# multiple files
mediainfo -pqt *.jpg *.png

# compare 2 images
mediainfo -diff image1.jpg image2.png
```

---

## Output Examples

### `-pt` (Photo Template)
```
Image;{"@type": "Image", "Format": "JPEG", "Width": "1496", "Height": "2232", "Compression_Mode": "Lossy", "BitDepth": "8", "4:4:4": null}
General;{"@type": "General", "FileSize": "411.00 KiB", "Comment": null}
```

### `-pqt` (Photo Quality Template)
```
Image;{"@type": "Image", "Format": "PNG", "Width": "1534", "Height": "2048", "Compression_Mode": "Lossless", "BitDepth": "8", "4:4:4": null}
General;{"@type": "General", "FileSize": "1.99 MiB", "Comment": null}
Quality;{@type: Quality, image.png | Brightness= 27761.20 | Contrast= 20864.90 | Balance= -0.09 | Verdict= Good | Resolution= 1534x2048 | Quality= 92 | sha256= b4ae73f1...}
```

### `-vt` (Video Template)
```
Video;{"@type": "Video", "Format": "H264", "Width": "1920", "Height": "1080", "FrameRate": "30.000", "4:4:4": "yuv420p"}
General;{"@type": "General", "FileSize": "1.20 GiB", "TBR": "5000000 b/s", "vid_url": null, "vid_md5": null, "vid_sha256": null, "vid_sha512": null}
```

### `-diff` (Image Diff)
```json
{"@type": "Diff",
  "File1": "image1.jpg",
  "File2": "image2.png",
  "Size1": "1496x2232",
  "Size2": "1496x2232",
  "Resized": false,
  "BBox": "(0, 0, 1496, 2232)",
  "MeanDiff": 3.1245,
  "MaxDiff": 48,
  "DiffPixels": 12453,
  "TotalPixels": 3339072,
  "DiffPercent": 0.3729,
  "Similarity": 0.9877
}
```

---

## Quality Verdict Rules

| Condition | Verdict |
|-----------|---------|
| `Brightness < 13000` | Too Dark |
| `Brightness > 50000` | Too Bright |
| `Contrast < 5000` | Low Contrast/Blurry |
| All pass | Good |

---

## Installation

### Dependencies

```bash
sudo apt install ffmpeg imagemagick libimage-exiftool-perl
```

### Build Binary

```bash
pip install pyinstaller Pillow numpy
cd mediainfo_tool
pyinstaller --onefile --paths . --name mediainfo main.py
sudo cp dist/mediainfo /usr/local/bin/mediainfo
sudo chmod +x /usr/local/bin/mediainfo
```

---

## Project Structure

```
mediainfo_tool/
├── main.py               # CLI entry point
├── mediainfo_tool.py     # Core logic and output formatting
├── models.py             # Data classes and enums
└── backends/
    ├── __init__.py
    ├── exiftool.py       # Image metadata + binary header reader
    ├── ffprobe.py        # Video metadata
    ├── magick.py         # Image quality analysis
    └── diff.py           # Image comparison
```

---

## Notes

- Filenames starting with `-` are handled correctly
- Dependency check runs on startup, missing tools are reported with install instructions
- Compression mode (Lossy/Lossless) is determined by reading the binary file header directly, not by file extension
