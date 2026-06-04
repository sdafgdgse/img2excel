"""
img_utils - 图片预处理工具
提供多种图片增强策略，专门针对模糊/不清/光线差的图片
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter


def upscale(image: Image.Image, scale: float = 2.0) -> Image.Image:
    """放大图片（对小文字场景有效）"""
    w, h = image.size
    return image.resize((int(w * scale), int(h * scale)), Image.LANCZOS)


def adaptive_threshold(image: Image.Image, block_size: int = 31, c: int = 10) -> Image.Image:
    """自适应阈值二值化（处理光线不均的图片）"""
    img_cv = np.array(image.convert("L"))
    binary = cv2.adaptiveThreshold(
        img_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, block_size, c
    )
    return Image.fromarray(binary)


def otsu_threshold(image: Image.Image) -> Image.Image:
    """Otsu 自动阈值二值化"""
    img_cv = np.array(image.convert("L"))
    _, binary = cv2.threshold(img_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(binary)


def denoise(image: Image.Image, strength: int = 10) -> Image.Image:
    """去噪（去除背景噪点）"""
    img_cv = np.array(image.convert("L"))
    denoised = cv2.fastNlMeansDenoising(img_cv, None, strength, 7, 21)
    return Image.fromarray(denoised)


def deskew(image: Image.Image) -> Image.Image:
    """自动纠偏（矫正倾斜的文字）"""
    img_cv = np.array(image.convert("L"))
    # 二值化
    _, binary = cv2.threshold(img_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # 找所有文字轮廓
    coords = np.column_stack(np.where(binary > 0))
    if len(coords) < 10:
        return image
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = 90 + angle
    # 纠偏
    h, w = img_cv.shape
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img_cv, matrix, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return Image.fromarray(rotated)


def sharpen(image: Image.Image, factor: float = 1.5) -> Image.Image:
    """锐化"""
    return image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))


def super_resolution(image: Image.Image) -> Image.Image:
    """简单超分辨率（放大+锐化，改善模糊图片）"""
    w, h = image.size
    # 逐步放大，效果更好
    img = image.resize((int(w * 1.5), int(h * 1.5)), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=200, threshold=2))
    return img


def preprocess_standard(image_path: str) -> Image.Image:
    """标准预处理：灰度 → 对比度增强 → 锐化"""
    img = Image.open(image_path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=5)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = img.filter(ImageFilter.SHARPEN)
    return img


def preprocess_aggressive(image_path: str) -> Image.Image:
    """激进预处理：放大 → 去噪 → 自适应二值化（适合模糊/光线差的图片）"""
    img = Image.open(image_path).convert("L")
    img = upscale(img, 2.0)
    img = denoise(img, 15)
    img = adaptive_threshold(img)
    return img


def preprocess_otsu(image_path: str) -> Image.Image:
    """Otsu 二值化预处理（适合扫描件）"""
    img = Image.open(image_path).convert("L")
    img = upscale(img, 1.5)
    img = sharp(img)
    img = otsu_threshold(img)
    return img


def try_best_preprocessing(image_path: str, ocr_func) -> tuple:
    """
    尝试多种预处理策略，返回 OCR 结果最好的那个。
    ocr_func: 接受图片路径，返回 [(text, bbox, conf), ...]
    """
    strategies = {
        "标准": preprocess_standard,
        "增强(去噪+自适应)": preprocess_aggressive,
        "二值化(Otsu)": preprocess_otsu,
    }

    best_items = []
    best_score = 0
    best_name = ""

    for name, method in strategies.items():
        try:
            img = method(image_path)
            tmp_path = image_path.rsplit(".", 1)[0] + f"_{name}.png"
            img.save(tmp_path)
            items = ocr_func(tmp_path)
            score = sum(conf for _, _, conf in items) / max(len(items), 1)
            if score > best_score:
                best_score = score
                best_items = items
                best_name = name
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            continue

    return best_items, best_name, best_score