from PIL import Image, ImageChops
import numpy as np

def compare(path1: str, path2: str) -> dict:
    img1 = Image.open(path1).convert('RGB')
    img2 = Image.open(path2).convert('RGB')

    # resize img2 về cùng size img1 nếu khác nhau
    if img1.size != img2.size:
        img2 = img2.resize(img1.size, Image.LANCZOS)
        resized = True
    else:
        resized = False

    diff = ImageChops.difference(img1, img2)
    arr = np.array(diff)

    bbox = diff.getbbox()
    mean_diff = float(arr.mean())
    max_diff = int(arr.max())
    diff_pixels = int(np.sum(arr.max(axis=2) > 10))
    total_pixels = img1.size[0] * img1.size[1]
    diff_percent = diff_pixels / total_pixels * 100

    # similarity score 0.0 - 1.0
    similarity = 1.0 - (mean_diff / 255.0)

    return {
        'file1': path1,
        'file2': path2,
        'size1': f"{img1.size[0]}x{img1.size[1]}",
        'size2': f"{img2.size[0]}x{img2.size[1]}",
        'resized': resized,
        'bbox': str(bbox),
        'mean_diff': round(mean_diff, 4),
        'max_diff': max_diff,
        'diff_pixels': diff_pixels,
        'total_pixels': total_pixels,
        'diff_percent': round(diff_percent, 4),
        'similarity': round(similarity, 4),
    }

def format_diff(data: dict) -> str:
    lines = [
        f'{{"@type": "Diff",',
        f'  "File1": "{data["file1"]}",',
        f'  "File2": "{data["file2"]}",',
        f'  "Size1": "{data["size1"]}",',
        f'  "Size2": "{data["size2"]}",',
        f'  "Resized": {str(data["resized"]).lower()},',
        f'  "BBox": "{data["bbox"]}",',
        f'  "MeanDiff": {data["mean_diff"]},',
        f'  "MaxDiff": {data["max_diff"]},',
        f'  "DiffPixels": {data["diff_pixels"]},',
        f'  "TotalPixels": {data["total_pixels"]},',
        f'  "DiffPercent": {data["diff_percent"]},',
        f'  "Similarity": {data["similarity"]}',
        f'}}',
    ]
    return '\n'.join(lines)
