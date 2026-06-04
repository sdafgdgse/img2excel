---
name: img2excel
description: "图片内容识别与分析。当用户提供图片并希望AI读取图片中的文字内容后，根据用户需求进行分析、回答或生成Excel时使用。流程：OCR提取文字 → AI理解内容 → 按需输出。支持中英文。触发词：图片转Excel、图片转表格、提取表格、OCR转Excel、截图转表格、帮我看看这张图、读取这张图片、图片里写了什么、分析这张图、把这张图转成表格、识别图片、看图说话"
---

# img2excel - 图片内容识别与分析

## 概述

当用户提供图片并提出需求时，先通过 OCR 提取图片中的文字，再将文字内容交给 AI 分析处理，按用户需求输出结果。

**核心理念：** 图片 → OCR 提取文字 → AI 理解内容 → 按需输出

## 安装依赖

```bash
pip install easyocr pillow openpyxl numpy
```

## 工作流程

### 第一步：检查图片

确认图片存在且格式支持（jpg/png/bmp/tiff/webp）。

### 第二步：OCR 提取文字

调用 OCR 提取图片中所有文字及其坐标：

```python
from scripts.img2excel import extract_text_from_image, extract_text_flat

# 获取带坐标的详细结果（用于表格检测）
items = extract_text_from_image("图片路径.jpg")

# 或仅获取纯文本（用于AI分析）
text = extract_text_flat("图片路径.jpg")
```

### 第三步：AI 分析

根据用户需求决定输出方式：

| 用户需求 | 处理方式 |
|---------|---------|
| "转成Excel" → | `detect_table_structure()` 推断行列 → `create_excel()` 生成 |
| "提取文字/写了什么" → | 直接返回 OCR 提取的文本 |
| "总结/分析/回答" → | 将 OCR 文本 + 用户问题交给 AI 综合分析 |
| "提取某个数据" → | 将 OCR 文本交给 AI 查找并回答 |

### 核心函数

```python
# 1. 纯文本提取（推荐给AI分析用）
all_text = extract_text_flat("图片.jpg")
# 返回: "识别的文字1\n识别的文字2\n..."

# 2. 带坐标的详细结果（用于表格检测）
items = extract_text_from_image("图片.jpg")
# 返回: [("文字", [(x1,y1),(x2,y2),(x3,y3),(x4,y4)], 置信度)]

# 3. 图片预处理（增强对比度）
enhanced = enhance_image("图片.jpg")

# 4. 生成Excel（仅在用户要求转表格时）
create_excel(table_data, "输出.xlsx")
```

## 处理原则

1. **先 OCR，再分析** — 先用 EasyOCR 提取文字，再让 AI 理解
2. **按需输出** — 用户要 Excel 才生成，要回答就直接回答
3. **自动清理** — 临时处理的图片文件会自动删除
4. **失败处理** — OCR 为空时提示用户检查图片清晰度

## 注意事项

- 首次运行 EasyOCR 会自动下载识别模型（约 50MB），需要网络
- 图片越清晰，识别效果越好
- 表格越规整（行列对齐），Excel 生成越准确
- 支持格式：jpg、png、bmp、tiff、webp