"""
img_utils - 图片预处理工具
提供对比度增强、二值化、自适应预处理等功能
"""

from PIL import Image, ImageEnhance, ImageOps, ImageFilter


def autocontrast(image_path: str, cutoff: int = 5) -> Image.Image:
    """自适应对比度增强"""
    img = Image.open(image_path)
    return ImageOps.autocontrast(img.convert("L"), cutoff=cutoff)


def binarize(image: Image.Image, threshold: int = 140) -> Image.Image:
    """二值化处理"""
    if image.mode != "L":
        image = image.convert("L")
    return image.point(lambda x: 0 if x < threshold else 255)


def enhance(image: Image.Image, factor: float = 2.0) -> Image.Image:
    """增加对比度"""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def preprocess(image_path: str, output_path: str = None) -> str:
    """完整预处理管道：增强 → 二值化"""
    img = Image.open(image_path)
    img = img.convert("L")
    img = ImageOps.autocontrast(img, cutoff=5)
    img = enhance(img, 1.5)
    img = img.filter(ImageFilter.SHARPEN)

    if output_path is None:
        output_path = image_path.rsplit(".", 1)[0] + "_processed.jpg"

    img.save(output_path, quality=95)
    return output_path