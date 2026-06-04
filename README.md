# img2excel

> 🖼️ → 🤖 给 AI 装上"眼睛"：看懂图片，回答问题，生成Excel

**img2excel** 是一个 Claude Code Skill。你把图片发给 AI，提出需求，AI 自动完成：**OCR 识图 → 理解内容 → 按你的要求处理**。

## 能做什么

| 你说 | AI 做的事 |
|------|----------|
| "这张发票总金额是多少？" | OCR提取 → AI找到金额 → 回答你 |
| "帮我把这个表格转成Excel" | OCR提取 → 检测行列 → 生成 .xlsx |
| "总结一下这张图的内容" | OCR提取 → AI理解 → 给你总结 |
| "分析这个数据表的趋势" | OCR提取 → AI分析 → 给出结论 |
| "这张图里写了什么" | OCR提取 → 全部读出 |

## 快速开始

```bash
# 装依赖
pip install easyocr pillow openpyxl numpy

# 直接发图片给AI + 提需求即可
```

## 文件结构

```
img2excel/
├── SKILL.md                 # → 核心：教AI如何识图 + 分析处理
├── scripts/
│   ├── img2excel.py         # OCR识别 + 表格检测 + Excel生成
│   └── img_utils.py         # 图片增强预处理
├── examples/
│   └── basic-usage.md       # 使用示例
└── references/
    └── setup.md             # 安装指引
```

## 技术原理

```
用户发图片 + 提需求
       ↓
Pillow 增强对比度 / 二值化 / 锐化
       ↓
EasyOCR 提取文字 + 坐标信息
       ↓
AI 理解OCR结果 + 用户需求
       ↓
按需输出：回答 / Excel / 分析结论
```

## 本次升级内容

- ✅ 支持提问式交互（不只是转Excel，还能回答、分析、总结）
- ✅ 增强表格检测算法（自动计算行间距阈值，聚类更准确）
- ✅ 文字清洗（过滤OCR常见噪音字符）
- ✅ 自动清理临时文件
- ✅ 支持更多图片格式（jpg/png/bmp/tiff/webp）
- ✅ 更好的错误提示

## 注意事项

- ⚡ 首次运行会下载约50MB的OCR模型，需要网络
- ✅ 图片越清晰、表格越规整，效果越准
- 🔧 识别失败时 AI 会提示你调整图片后重试

## License

MIT