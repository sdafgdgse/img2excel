# img2excel

> 🖼️ → 🤖 给 AI 一双"眼睛"：看懂图片，回答问题，生成Excel

**img2excel** 是一个 Claude Code Skill —— 你甩一张图片给 AI，再提需求，AI 自动：**OCR 识图 → 理解内容 → 按你的要求处理**

## 使用场景

| 你说 | AI 做的事 |
|------|----------|
| "帮我看一下这张发票的总金额" | OCR提取 → 找到金额数字 → 回答你 |
| "把这张表格转成Excel" | OCR提取 → 检测行列 → 生成 .xlsx |
| "帮我总结一下这张图的内容" | OCR提取 → 理解语义 → 给你总结 |
| "分析这个表格的数据趋势" | OCR提取 → 分析数据 → 给出结论 |
| "这张图里写了什么" | OCR提取 → 全部读出 |

## 快速开始

```bash
# 装依赖
pip install easyocr pillow openpyxl numpy

# 给 AI 发图片 + 提需求即可
```

## 文件一览

```
img2excel/
├── SKILL.md                 # 核心：教AI如何识图 + 分析处理
├── scripts/img2excel.py     # OCR识别 + 表格检测 + Excel生成
├── scripts/img_utils.py     # 图片增强预处理
└── references/setup.md      # 安装指引
```

## 技术原理

```
用户发图片 + 提需求
       ↓
Pillow 增强图片对比度
       ↓
EasyOCR 提取文字 + 坐标信息
       ↓
AI 理解OCR结果 + 用户需求
       ↓
按需输出：回答 / Excel / 分析结论
```

## 注意事项

- ⚡ 首次运行会下载约50MB的OCR模型，需要网络
- ✅ 图片越清晰，识别效果越好
- 🔧 识别失败时 AI 会提示你调整图片后重试

## License

MIT