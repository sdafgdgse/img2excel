# img2excel

> 🖼️ → 📊 给 AI 一双眼睛：把图片里的表格直接变成 Excel

**img2excel** 是一个 Claude Code Skill —— 你甩一张图片给 AI，说"转成Excel"，它自动完成 OCR 识别 → 表格检测 → Excel 生成。

## 适用场景

| 场景 | 例子 |
|------|------|
| 📸 截图转表格 | 网页数据截图 → 可直接编辑的Excel |
| 📄 扫描件转电子档 | 纸质报表扫描件 → 数字表格 |
| 🧾 单据信息提取 | 发票、收据拍照 → 结构化数据 |
| 📊 数据报表整理 | 图表中的数字 → 可计算的Excel |

## 快速开始

```bash
# 1. 装依赖
pip install easyocr pillow openpyxl numpy

# 2. 给 AI 发一张图片，说：
#    "帮我把这张图片转成Excel"
```

## 文件一览

```
img2excel/
├── SKILL.md              # → 核心：教AI怎么处理图片转Excel
├── scripts/img2excel.py  # OCR识别 + 表格检测 + Excel生成
├── scripts/img_utils.py  # 图片增强预处理
└── references/setup.md   # 安装指引
```

## 技术原理

```
图片 → Pillow增强对比度 → EasyOCR提取文字 + 坐标
                                          ↓
                                   分析行列结构
                                          ↓
                              openpyxl生成格式化Excel
```

## 注意事项

- ⚡ 首次运行会下载约50MB的OCR模型，需要网络
- ✅ 图片越清晰、表格越规整，识别越准
- 🔧 识别失败时 AI 会提示你调整图片后重试

## License

MIT