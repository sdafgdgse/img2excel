"""
img2excel - 图片转Excel表格 / 图片文字识别与智能分析
将图片中的表格数据通过OCR识别后导出为格式化的Excel文件，
或提取图片中的全部文字供AI分析处理。
"""

import os
import sys
import tempfile
import argparse
from pathlib import Path


def extract_text_from_image(image_path: str, smart: bool = True) -> list:
    """使用OCR从图片提取文字，返回 (text, bbox, confidence) 列表

    参数:
        smart: True = 自动尝试多种预处理方案选最佳（适合模糊/光线差的图片）
    """
    try:
        import easyocr
    except ImportError:
        print("正在安装 easyocr...")
        os.system(f"{sys.executable} -m pip install easyocr")
        import easyocr

    reader = easyocr.Reader(["ch_sim", "en"], gpu=False)

    if smart:
        return _smart_extract(image_path, reader)

    items = reader.readtext(image_path, detail=1, paragraph=False)
    return [(text, bbox, conf) for bbox, text, conf in items if conf > 0.25]


def _smart_extract(image_path: str, reader) -> list:
    """
    智能OCR提取：尝试多种预处理策略，返回置信度最高的结果。
    针对模糊、光线差、倾斜等场景优化。
    """
    import scripts.img_utils as img_utils

    best_items = []
    best_score = 0
    best_name = "原始"

    # 策略1: 直接用原图
    try:
        items = reader.readtext(image_path, detail=1, paragraph=False)
        items = [(t, b, c) for t, b, c in items if c > 0.2]
        score = sum(c for _, _, c in items) / max(len(items), 1) if items else 0
        if score > best_score:
            best_score, best_items, best_name = score, items, "原图"
    except Exception:
        pass

    # 策略2-4: 使用 img_utils 的多种预处理
    def try_method(name, method):
        nonlocal best_items, best_score, best_name
        try:
            img = method(image_path)
            fd, tmp = tempfile.mkstemp(suffix=f"_{name}.png")
            os.close(fd)
            img.save(tmp)
            items = reader.readtext(tmp, detail=1, paragraph=False)
            items = [(t, b, c) for t, b, c in items if c > 0.2]
            score = sum(c for _, _, c in items) / max(len(items), 1) if items else 0
            if score > best_score:
                best_score, best_items, best_name = score, items, name
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass

    try_method("自适应二值化", img_utils.preprocess_aggressive)
    try_method("Otsu二值化", img_utils.preprocess_otsu)
    try_method("超分辨率", lambda p: img_utils.super_resolution(img_utils.preprocess_standard(p)))
    try_method("纠偏", lambda p: img_utils.deskew(img_utils.preprocess_standard(p)))

    return best_items


def extract_text_flat(image_path: str) -> str:
    """OCR提取纯文本（不含坐标），供AI分析使用"""
    items = extract_text_from_image(image_path, smart=True)
    return "\n".join(text for text, _, _ in items)


def clean_text(text: str) -> str:
    """清洗OCR识别结果中的常见噪音"""
    import re
    text = re.sub(r"[|｜lI]", "1", text)
    text = re.sub(r"[Oo0]", "0", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_table_structure(items: list) -> list:
    """根据文本坐标检测表格行列结构（增强版）"""
    if not items:
        return []

    # 过滤低置信度
    items = [(text, bbox, conf) for text, bbox, conf in items if conf > 0.3]
    if not items:
        return []

    # 统计Y坐标间距，自动计算行聚类阈值
    y_centers = sorted([(bbox[0][1] + bbox[2][1]) / 2 for _, bbox, _ in items])
    gaps = []
    for i in range(1, len(y_centers)):
        gap = y_centers[i] - y_centers[i - 1]
        if gap > 5:
            gaps.append(gap)
    y_threshold = max(25, min(gaps) * 1.5) if gaps else 30

    # 按Y轴聚类为行
    rows = {}
    for text, bbox, conf in items:
        y_center = (bbox[0][1] + bbox[2][1]) / 2
        x_center = (bbox[0][0] + bbox[1][0]) / 2
        text = clean_text(text)
        matched = False
        closest_key = None
        closest_dist = float("inf")
        for key in rows:
            dist = abs(y_center - key)
            if dist < y_threshold and dist < closest_dist:
                closest_key = key
                closest_dist = dist
                matched = True
        if matched:
            rows[closest_key].append((x_center, text))
        else:
            rows[y_center] = [(x_center, text)]

    # 排序输出
    sorted_rows = sorted(rows.items(), key=lambda x: x[0])
    table_data = []
    for _, row_items in sorted_rows:
        row_items.sort(key=lambda x: (x[0]))
        table_data.append([item[1] for item in row_items])

    return table_data


def create_excel(table_data: list, output_path: str) -> str:
    """将表格数据写入格式化的Excel文件"""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    header_fill = PatternFill("solid", fgColor="4472C4")
    header_font = Font(name="Arial", bold=True, color="FFFFFF", size=11)
    body_font = Font(name="Arial", size=10)
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )

    for row_idx, row_data in enumerate(table_data, 1):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.font = header_font if row_idx == 1 else body_font
            if row_idx == 1:
                cell.fill = header_fill
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center", wrap_text=True)

    for col in ws.columns:
        max_len = max(
            (len(str(cell.value or "")) for cell in col if cell.value), default=10
        )
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 45)

    wb.save(output_path)
    return output_path


def enhance_image(image_path: str) -> str:
    """增强图片对比度，提高OCR识别率"""
    from PIL import Image, ImageEnhance, ImageOps, ImageFilter

    img = Image.open(image_path)
    img = img.convert("L")
    img = ImageOps.autocontrast(img, cutoff=3)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = img.filter(ImageFilter.SHARPEN)

    fd, enhanced_path = tempfile.mkstemp(suffix="_enhanced.png")
    os.close(fd)
    img.save(enhanced_path, format="PNG")
    return enhanced_path


def get_output_path(image_path: str, output_path: str = None) -> str:
    """确定输出Excel路径"""
    if output_path:
        return output_path
    filename = os.path.splitext(os.path.basename(image_path))[0]
    return os.path.join("D:\\", f"{filename}.xlsx")


def img2excel(image_path: str, output_path: str = None) -> str:
    """主函数：图片 → Excel（完整流程）"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片不存在: {image_path}")

    SUPPORTED = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp")
    if not image_path.lower().endswith(SUPPORTED):
        raise ValueError(f"不支持的图片格式，支持: {', '.join(SUPPORTED)}")

    output_path = get_output_path(image_path, output_path)

    print(f"[1/3] 图片预处理...")
    enhanced = enhance_image(image_path)

    try:
        print(f"[2/3] OCR识别中...")
        items = extract_text_from_image(enhanced)
        if not items:
            raise RuntimeError("未能从图片中识别到文字。请确保图片清晰、文字可辨，或尝试重新截图。")

        print(f"[3/3] 分析行列结构，生成Excel...")
        table = detect_table_structure(items)
        if not table:
            raise RuntimeError("未能检测到表格结构。")

        result = create_excel(table, output_path)
        print(f"✅ 完成! 已生成: {result}")
        print(f"   识别到 {len(table)} 行数据")
        return result
    finally:
        # 清理临时文件
        if os.path.exists(enhanced):
            try:
                os.remove(enhanced)
            except OSError:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="img2excel - 图片转Excel表格")
    parser.add_argument("image", help="图片文件路径（支持jpg/png/bmp/tiff/webp）")
    parser.add_argument("-o", "--output", help="输出Excel路径（默认D盘）")
    args = parser.parse_args()

    try:
        img2excel(args.image, args.output)
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}", file=sys.stderr)
        sys.exit(1)