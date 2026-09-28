import subprocess

def read(path: str) -> dict:
    # dung cong thuc chuan tu mediainfo_func
    result = subprocess.run(
        ['magick', 'identify', '-colorspace', 'Gray', '-format',
         '%[mean]|%[standard-deviation]|%[skewness]|%[kurtosis]|%w|%h|%Q',
         '--', path],
        capture_output=True, text=True
    )
    parts = result.stdout.strip().split('|')
    if len(parts) < 7:
        return {}

    mean    = float(parts[0])
    std     = float(parts[1])
    skew    = float(parts[2])
    # kurt  = float(parts[3])  # khong dung
    width   = parts[4]
    height  = parts[5]
    quality = parts[6]

    # verdict
    issues = []
    if mean < 13000:
        issues.append('Too Dark')
    elif mean > 50000:
        issues.append('Too Bright')
    if std < 5000:
        issues.append('Low Contrast/Blurry')
    verdict = 'Good' if not issues else ', '.join(issues)

    brightness = round(mean, 2)
    contrast   = round(std, 2)
    balance    = round(skew, 2)

    # sha256
    sha256 = subprocess.run(
        ['sha256sum', '--', path],
        capture_output=True, text=True
    ).stdout.split()[0]

    return {
        'brightness': brightness,
        'contrast': contrast,
        'balance': balance,
        'verdict': verdict,
        'quality': quality,
        'width': width,
        'height': height,
        'sha256': sha256,
    }
