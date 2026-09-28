from dataclasses import dataclass
from typing import Optional
from enum import Enum

class OutputMode(Enum):
    VT = "vt"    # video template
    PT = "pt"    # photo template
    PQT = "pqt"  # photo quality template
    DIFF = "diff" # compare 2 images

@dataclass
class MediaInfo:
    filename: str
    file_size: str
    width: Optional[str]
    height: Optional[str]
    format: Optional[str]
    # video
    frame_rate: Optional[str]
    overall_bitrate: Optional[str]
    chroma_subsampling: Optional[str]
    vid_url: Optional[str]
    vid_md5: Optional[str]
    vid_sha256: Optional[str]
    vid_sha512: Optional[str]
    # image
    compression_mode: Optional[str]
    bit_depth: Optional[str]
    comment: Optional[str]
    # quality
    quality: Optional[str]
    brightness: Optional[str]
    contrast: Optional[str]
    balance: Optional[str]
    verdict: Optional[str]
    sha256: Optional[str]
    is_image: bool
