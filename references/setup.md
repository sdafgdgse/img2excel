# img2excel 环境安装指南

## 系统要求

- Python 3.8+
- Windows / macOS / Linux

## 安装步骤

### 1. 安装依赖

```bash
pip install easyocr pillow openpyxl numpy opencv-python
```

各包作用：

| 包名 | 版本要求 | 用途 |
|------|---------|------|
| easyocr | >=1.7 | OCR 文字识别（中英文） |
| pillow | >=10.0 | 图片预处理 |
| openpyxl | >=3.1 | Excel 文件生成 |
| numpy | >=1.24 | 坐标数据处理 |
| opencv-python | >=4.8 | 高级图像处理（去噪、纠偏、自适应阈值） |

### 2. 验证安装

```bash
python -c "from scripts.img2excel import img2excel; print('安装成功')"
```

### 3. 首次运行说明

首次调用 EasyOCR 时会自动下载识别模型（约50MB），请确保网络畅通：

```
Downloading detection model, please wait...
Downloading recognition model, please wait...
```

模型下载完成后会自动缓存，后续使用无需再次下载。

## 安装到 Claude Code

将项目目录复制到目标项目的 `.claude/skills/` 下：

```bash
cp -r img2excel /your-project/.claude/skills/
```

## 常见问题

**Q: EasyOCR 下载模型失败怎么办？**
A: 请检查网络连接，或设置代理后重试。

**Q: 识别结果乱码？**
A: 确保安装了中文字体，并确认 `lang='ch_sim'` 参数正确。

**Q: 生成的Excel格式不对？**
A: 尝试提高图片质量，确保表格线条清晰，文字对齐。