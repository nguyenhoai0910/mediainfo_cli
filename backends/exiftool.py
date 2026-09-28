import subprocess, json, os

def get_compression_mode(path: str) -> str:
    """Đọc binary header để xác định Lossy/Lossless chính xác."""
    try:
        with open(path, 'rb') as f:
            header = f.read(16)

        # JPEG: FFD8
        if header[:2] == b'\xff\xd8':
            with open(path, 'rb') as f:
                data = f.read()
            if b'\xff\xc3' in data:
                return 'Lossless'
            return 'Lossy'

        # PNG
        if header[:8] == b'\x89PNG\r\n\x1a\n':
            return 'Lossless'

        # WEBP
        if header[:4] == b'RIFF' and header[8:12] == b'WEBP':
            chunk = header[12:16]
            if chunk == b'VP8L':
                return 'Lossless'
            elif chunk[:3] == b'VP8':
                return 'Lossy'
            elif chunk == b'VP8X':
                with open(path, 'rb') as f:
                    content = f.read()
                if b'VP8L' in content:
                    return 'Lossless'
                return 'Lossy'

        # BMP
        if header[:2] == b'BM':
            return 'Lossless'

        # GIF
        if header[:6] in (b'GIF87a', b'GIF89a'):
            return 'Lossless'

        # TIFF
        if header[:2] in (b'II', b'MM'):
            return 'Lossless'

        # JPEG2000
        if header[:12] == b'\x00\x00\x00\x0cjP  \r\n\x87\n':
            return 'Lossless or Lossy'

    except Exception:
        pass

    return 'Unknown'


def format_size_mib(path: str) -> str:
    """Đọc size thật từ filesystem và convert sang MiB."""
    size_bytes = os.path.getsize(path)
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.2f} MiB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KiB"
    return f"{size_bytes} B"


def read(path: str) -> dict:
    result = subprocess.run(
        ['exiftool', '-j',
         '-ImageWidth', '-ImageHeight',
         '-FileType', '-BitDepth', '-BitsPerSample',
         '-YCbCrSubSampling', '-Comment',
         '--', path],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)[0]

    return {
        'file_size': format_size_mib(path),
        'width': str(data.get('ImageWidth', '')),
        'height': str(data.get('ImageHeight', '')),
        'format': data.get('FileType', ''),
        'compression_mode': get_compression_mode(path),
        'bit_depth': str(data.get('BitDepth') or data.get('BitsPerSample') or ''),
        'chroma_subsampling': data.get('YCbCrSubSampling'),
        'comment': data.get('Comment'),
    }
