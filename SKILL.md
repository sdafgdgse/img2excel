---
name: img2excel
description: "图片内容识别与分析。当用户提供图片并希望AI读取图片中的文字内容后进行分析、回答或转成Excel时使用。流程：OCR提取文字 → AI根据用户问题进行处理。支持中英文。触发词：图片转Excel、图片转表格、提取表格、OCR转Excel、截图转表格、帮我看看这张图、读取这张图片、图片里写了什么、分析这张图"
---

# img2excel - 图片内容识别与分析

## 概述

当用户提供图片并提出需求时，先通过 OCR 提取图片中的文字，再将文字内容交给 AI 分析处理。

**核心流程：** 图片 → OCR 提取文字 → AI 理解内容 → 按用户要求输出

## 安装依赖

```bash
pip install easyocr pillow openpyxl numpy
```

## 工作流程

### 第一步：OCR 提取文字

当用户上传图片时，调用 OCR 提取图片中所有文字：

```python
from scripts.img2excel import extract_text_from_image

items = extract_text_from_image("用户图片路径.jpg")
# items = [(text, bbox, confidence), ...]
```

### 第二步：AI 分析处理

将提取的文字内容 + 用户的问题，交给 AI 综合分析：

```
用户问题: "把这张表转成Excel"
OCR文字: [提取到的表格数据]
→ AI: 整理为 .xlsx 文件

用户问题: "这张发票的总金额是多少？"
OCR文字: [发票上的文字]
→ AI: 提取并回答总金额

用户问题: "帮我看一下这个表格的趋势"
OCR文字: [表格数据]
→ AI: 分析数据趋势并给出结论
```

### 第三步：按需输出结果

根据用户需求决定输出格式：

| 用户需求 | 输出方式 |
|---------|---------|
| "转成Excel" | 调用 `create_excel()` 生成 .xlsx |
| "总结一下" | 直接文字回答 |
| "提取某个数据" | 直接回答 |
| "分析趋势" | 文字分析 + 可选的图表 |

## 函数说明

```python
# 1. OCR 提取文字（核心）
items = extract_text_from_image("图片路径")
# 返回: [("识别的文字", [(x1,y1),...], 置信度), ...]

# 2. 图片预处理（提高识别率）
enhanced_path = enhance_image("图片路径")

# 3. 生成 Excel（仅在用户要求时）
create_excel(table_data, "输出路径.xlsx")
```

## 处理原则

1. **先 OCR，再分析** — 先用 OCR 提取文字，再结合用户问题让 AI 理解
2. **按需输出** — 用户要Excel才生成Excel，要回答就直接回答
3. **原始文字保留** — 提取的文字尽量完整，交给 AI 分析筛选
4. **失败处理** — OCR 为空时提示用户检查图片清晰度

## 注意事项

- 首次运行 EasyOCR 会自动下载模型（约 50MB）
- 图片越清晰，识别效果越好
- OCR 提取的是原始文字 + 坐标信息，AI 负责理解和结构化