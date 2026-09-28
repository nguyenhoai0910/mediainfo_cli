from pathlib import Path
from models import MediaInfo, OutputMode
from backends import exiftool, ffprobe, magick

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif'}
VIDEO_EXTS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.m4v'}

def _opt(val):
    return f'"{val}"' if val else 'null'

def format_vt(info: MediaInfo) -> str:
    video = (
        f'{{"@type": "Video", "Format": "{info.format}", '
        f'"Width": "{info.width}", "Height": "{info.height}", '
        f'"FrameRate": "{info.frame_rate}", '
        f'"4:4:4": {_opt(info.chroma_subsampling)}}}'
    )
    general = (
        f'{{"@type": "General", "FileSize": "{info.file_size}", '
        f'"TBR": {_opt(info.overall_bitrate)}, '
        f'"vid_url": {_opt(info.vid_url)}, '
        f'"vid_md5": {_opt(info.vid_md5)}, '
        f'"vid_sha256": {_opt(info.vid_sha256)}, '
        f'"vid_sha512": {_opt(info.vid_sha512)}}}'
    )
    return f"Video;{video}\nGeneral;{general}"

def format_pt(info: MediaInfo) -> str:
    image = (
        f'{{"@type": "Image", "Format": "{info.format}", '
        f'"Width": "{info.width}", "Height": "{info.height}", '
        f'"Compression_Mode": "{info.compression_mode}", '
        f'"BitDepth": {_opt(info.bit_depth)}, '
        f'"4:4:4": {_opt(info.chroma_subsampling)}}}'
    )
    general = (
        f'{{"@type": "General", "FileSize": "{info.file_size}", '
        f'"Comment": {_opt(info.comment)}}}'
    )
    return f"Image;{image}\nGeneral;{general}"

def format_pqt(info: MediaInfo) -> str:
    image = (
        f'{{"@type": "Image", "Format": "{info.format}", '
        f'"Width": "{info.width}", "Height": "{info.height}", '
        f'"Compression_Mode": "{info.compression_mode}", '
        f'"BitDepth": {_opt(info.bit_depth)}, '
        f'"4:4:4": {_opt(info.chroma_subsampling)}}}'
    )
    general = (
        f'{{"@type": "General", "FileSize": "{info.file_size}", '
        f'"Comment": {_opt(info.comment)}}}'
    )
    quality = (
        f'{{@type: Quality, {info.filename} | '
        f'Brightness= {info.brightness} | '
        f'Contrast= {info.contrast} | '
        f'Balance= {info.balance} | '
        f'Verdict= {info.verdict} | '
        f'Resolution= {info.width}x{info.height} | '
        f'Quality= {info.quality} | '
        f'sha256= {info.sha256}}}'
    )
    return f"Image;{image}\nGeneral;{general}\nQuality;{quality}"

def read(path: str, mode: OutputMode = OutputMode.PT) -> str:
    ext = Path(path).suffix.lower()
    is_image = ext in IMAGE_EXTS

    if is_image:
        data = exiftool.read(path)
        if mode == OutputMode.PQT:
            magick_data = magick.read(path)
            data.update(magick_data)
    else:
        data = ffprobe.read(path)

    info = MediaInfo(
        filename=Path(path).name,
        is_image=is_image,
        file_size=data.get('file_size', ''),
        width=data.get('width'),
        height=data.get('height'),
        format=data.get('format'),
        frame_rate=data.get('frame_rate'),
        overall_bitrate=data.get('overall_bitrate'),
        chroma_subsampling=data.get('chroma_subsampling'),
        vid_url=data.get('vid_url'),
        vid_md5=data.get('vid_md5'),
        vid_sha256=data.get('vid_sha256'),
        vid_sha512=data.get('vid_sha512'),
        compression_mode=data.get('compression_mode'),
        bit_depth=data.get('bit_depth'),
        comment=data.get('comment'),
        quality=data.get('quality'),
        brightness=data.get('brightness'),
        contrast=data.get('contrast'),
        balance=data.get('balance'),
        verdict=data.get('verdict'),
        sha256=data.get('sha256'),
    )

    if mode == OutputMode.VT:
        return format_vt(info)
    elif mode == OutputMode.PT:
        return format_pt(info)
    elif mode == OutputMode.PQT:
        return format_pqt(info)
