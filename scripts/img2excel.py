"""
img2excel - 图片转Excel表格
将图片中的表格数据通过OCR识别后导出为格式化的Excel文件
"""

import os
import sys
import argparse
from pathlib import Path

def extract_text_from_image(image_path: str) -> list:
    """使用OCR从图片提取文本"""
    try:
        import easyocr
    except ImportError:
        print("正在安装 easyocr...")
        os.system(f"{sys.executable} -m pip install easyocr")
        import easyocr

    reader = easyocr.Reader(["ch_sim", "en"], gpu=False)
    result = reader.readtext(image_path, detail=1)
    return [(text, bbox, conf) for bbox, text, conf in result if conf > 0.3]


def detect_table_structure(items: list) -> list:
    """根据文本坐标检测表格行列结构"""
    if not items:
        return []

    rows = {}
    Y_THRESHOLD = 30

    for text, bbox, conf in items:
        y_center = (bbox[0][1] + bbox[2][1]) / 2
        x_center = (bbox[0][0] + bbox[1][0]) / 2
        matched = False
        for key in rows:
            if abs(y_center - key) < Y_THRESHOLD:
                rows[key].append((x_center, text))
                matched = True
                break
        if not matched:
            rows[y_center] = [(x_center, text)]

    sorted_rows = sorted(rows.items(), key=lambda x: x[0])
    table_data = []
    for _, row_items in sorted_rows:
        row_items.sort(key=lambda x: x[0])
        table_data.append([item[1] for item in row_items])

    return table_data


def create_excel(table_data: list, output_path: str):
    """将表格数据写入Excel文件"""
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
            cell.fill = header_fill if row_idx == 1 else PatternFill()
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center", wrap_text=True)

    for col in ws.columns:
        max_len = max((len(str(cell.value or "")) for cell in col), default=10)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 40)

    wb.save(output_path)
    return output_path


def enhance_image(image_path: str) -> str:
    """增强图片对比度，提高OCR识别率"""
    try:
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError:
        print("正在安装 pillow...")
        os.system(f"{sys.executable} -m pip install pillow")
        from PIL import Image, ImageEnhance, ImageOps

    img = Image.open(image_path)
    img = img.convert("L")
    img = ImageOps.autocontrast(img, cutoff=5)
    enhanced_path = image_path.rsplit(".", 1)[0] + "_enhanced.jpg"
    img.save(enhanced_path, quality=95)
    return enhanced_path


def img2excel(image_path: str, output_path: str = None) -> str:
    """主函数：图片→Excel"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片不存在: {image_path}")

    if output_path is None:
        output_path = os.path.join("D:\\", os.path.splitext(os.path.basename(image_path))[0] + ".xlsx")

    print(f"[1/3] 图片预处理...")
    enhanced = enhance_image(image_path)

    print(f"[2/3] OCR识别中...")
    items = extract_text_from_image(enhanced)
    if not items:
        raise RuntimeError("OCR未能识别到任何文字，请检查图片清晰度")

    print(f"[3/3] 生成Excel表格...")
    table = detect_table_structure(items)
    result = create_excel(table, output_path)

    print(f"完成! 已生成: {result}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="图片转Excel表格")
    parser.add_argument("image", help="图片文件路径")
    parser.add_argument("-o", "--output", help="输出Excel路径(默认D盘)")
    args = parser.parse_args()

    try:
        img2excel(args.image, args.output)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)