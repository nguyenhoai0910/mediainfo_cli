import hashlib
from tools import find_tool, run


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read(path: str) -> dict:
    result = run([find_tool('magick'), 'identify', '-colorspace', 'Gray', '-format',
                  '%[mean]|%[standard-deviation]|%[skewness]|%[kurtosis]|%w|%h|%Q',
                  '--', path])
    parts = result.stdout.strip().split('|')
    if len(parts) < 7:
        return {}

    mean = float(parts[0])
    std = float(parts[1])
    skew = float(parts[2])
    width = parts[4]
    height = parts[5]
    quality = parts[6]

    issues = []
    if mean < 13000:
        issues.append('Too Dark')
    elif mean > 50000:
        issues.append('Too Bright')
    if std < 5000:
        issues.append('Low Contrast/Blurry')
    verdict = 'Good' if not issues else ', '.join(issues)

    return {
        'brightness': round(mean, 2),
        'contrast': round(std, 2),
        'balance': round(skew, 2),
        'verdict': verdict,
        'quality': quality,
        'width': width,
        'height': height,
        'sha256': sha256_of(path),
    }
