# img2excel 使用示例

## 示例1：基本使用

用户提供一张图片路径，将其中的表格转成Excel。

**用户输入：**
```
帮我把这张图片转成Excel
D:/图片/发票截图.jpg
```

**处理流程：**

```python
from scripts.img2excel import img2excel

result = img2excel("D:/图片/发票截图.jpg")
# 输出: D:/发票截图.xlsx
```

## 示例2：指定输出路径

**用户输入：**
```
把这张表格图片转成Excel，保存到 D:/data/输出.xlsx
```

**处理流程：**

```python
from scripts.img2excel import img2excel

result = img2excel("表格截图.png", output_path="D:/data/输出.xlsx")
```

## 示例3：处理失败时

当 OCR 未能识别到文字时，告知用户：

> "未能从图片中识别到文字，请确保：
> 1. 图片清晰，文字可辨
> 2. 图片中有足够的对比度
> 3. 可以尝试重新截图或拍照"

## 示例4：批量处理

虽然核心功能聚焦单张图片，但可通过循环处理多张图片：

```python
import glob
from scripts.img2excel import img2excel

for img in glob.glob("D:/图片/*.jpg"):
    img2excel(img)
```