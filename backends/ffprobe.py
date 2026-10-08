import json
from tools import find_tool, run


def read(path: str) -> dict:
    result = run([find_tool('ffprobe'), '-v', 'error', '-print_format', 'json',
                  '-show_format', '-show_streams', path])
    info = json.loads(result.stdout)
    video = next((s for s in info.get('streams', []) if s.get('codec_type') == 'video'), {})
    fmt = info.get('format', {})
    tags = fmt.get('tags', {})

    size_bytes = int(fmt.get('size', 0))
    size_str = f"{size_bytes / 1024 / 1024:.1f} MiB"

    bitrate = fmt.get('bit_rate')
    bitrate_str = f"{bitrate} b/s" if bitrate else None

    fps_raw = video.get('r_frame_rate', '0/1')
    try:
        num, den = fps_raw.split('/')
        fps = f"{int(num) / int(den):.3f}"
    except Exception:
        fps = None

    return {
        'file_size': size_str,
        'width': str(video.get('width', '')),
        'height': str(video.get('height', '')),
        'format': video.get('codec_name', '').upper(),
        'frame_rate': fps,
        'overall_bitrate': bitrate_str,
        'chroma_subsampling': video.get('pix_fmt'),
        'vid_url': tags.get('vid_url'),
        'vid_md5': tags.get('vid_md5'),
        'vid_sha256': tags.get('vid_sha256'),
        'vid_sha512': tags.get('vid_sha512'),
    }
