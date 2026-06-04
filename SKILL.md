---
name: img2excel
description: "图片转Excel表格。当用户提供图片（截图、拍照、扫描件）并希望将其中的表格数据提取并整理为Excel文件时使用。支持中英文混合识别。触发词：图片转Excel、图片转表格、提取表格、OCR转Excel、截图转表格"
---

# img2excel - 图片转Excel表格

## 概述

将图片中的表格数据通过 OCR 识别后，自动整理为格式化的 Excel 文件 (.xlsx)。

## 安装依赖

```bash
pip install easyocr pillow openpyxl numpy
```

## 使用方法

用户提供图片路径时，执行以下流程：

```python
from scripts.img2excel import img2excel

# 基本使用（输出到D盘，自动命名）
result = img2excel("图片路径.jpg")

# 指定输出路径
result = img2excel("图片路径.png", output_path="D:/输出表格.xlsx")
```

## 工作流程

当用户请求"把这张图片转成Excel"时，按以下步骤执行：

1. **检查环境** — 确认 easyocr、pillow、openpyxl 已安装
2. **图片预处理** — 调用 `scripts/img2excel.enhance_image()` 增强对比度
3. **OCR 识别** — 调用 `scripts/img2excel.extract_text_from_image()` 提取文字
4. **表格检测** — 调用 `scripts/img2excel.detect_table_structure()` 根据坐标推断行列
5. **生成 Excel** — 调用 `scripts/img2excel.create_excel()` 输出格式化的 .xlsx
6. **返回结果** — 告知用户文件路径

## 错误处理

- OCR 识别结果为空的提示用户检查图片清晰度
- 输出路径不存在时尝试自动创建目录
- 依赖缺失时自动提示安装命令

## 注意事项

- 首次运行 EasyOCR 会自动下载识别模型（约 50MB），需要网络连接
- 建议图片清晰、文字与背景对比度高时效果最佳
- 表格结构越规整（有对齐的行列），识别准确率越高