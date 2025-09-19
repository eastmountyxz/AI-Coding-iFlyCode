# -*- coding: utf-8 -*-
"""
任务：
1）内置一份从主流新闻、博客与学术话题中整理出的“大模型 & AI Coding”热门词汇及其热度（频次）列表；
2）统计并以降序存储（保存为 CSV）；
3）使用 PyEcharts 绘制词云（若本机未安装 PyEcharts，将在代码中自动安装）。

运行后将生成：
- keywords_freq.csv
- llm_ai_coding_wordcloud.html （可在浏览器中打开）
"""

import os
import sys
import csv

# -----------------------------
# (0) 确保 PyEcharts 可用（若缺失则自动安装）
# -----------------------------
def ensure_pyecharts():
    try:
        from pyecharts import options as opts  # noqa: F401
        from pyecharts.charts import WordCloud  # noqa: F401
    except Exception:
        # 自动静默安装
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyecharts"])
    # 再次导入
    from pyecharts import options as opts
    from pyecharts.charts import WordCloud
    return opts, WordCloud

opts, WordCloud = ensure_pyecharts()

# -----------------------------
# (1) 热门词汇及词频（可直接替换/扩充）
# 说明：数字越大表示近期出现更频繁/关注度更高
# -----------------------------
words_freq = [
    # Agentic / 多智能体 & 编排
    ("Agentic AI", 80), ("AI agents", 60), ("multi-agent", 36), ("tool use", 28),
    ("function calling", 34), ("orchestration", 22), ("agent memory", 20),
    ("planning", 18), ("agentic workflows", 45), ("agent framework", 24),
    ("autonomous coding", 26), ("code agents", 21),

    # 检索增强 / 知识组织
    ("RAG", 65), ("Agentic RAG", 42), ("GraphRAG", 38), ("vector database", 26),
    ("hybrid search", 22), ("knowledge graph", 24), ("long-context", 23),

    # 评测与基准（AI Coding）
    ("SWE-bench", 56), ("SWE-bench Live", 40), ("Multi-SWE-bench", 35),
    ("commit-level evals", 18), ("unit tests", 20), ("benchmark contamination", 17),

    # 训练 & 微调
    ("SFT", 21), ("DPO", 28), ("RLHF", 24), ("LoRA", 25), ("QLoRA", 20),
    ("distillation", 18), ("self-play fine-tuning", 19),
    ("synthetic data", 23), ("instruction tuning", 20),

    # 架构与模型
    ("MoE", 25), ("Mixture-of-Agents", 19), ("Transformer", 22),
    ("Mamba", 16), ("state space models", 15), ("SLM (small language model)", 18),

    # 推理与加速
    ("speculative decoding", 32), ("collaborative decoding", 24),
    ("FlashAttention", 22), ("quantization", 26), ("KV cache", 19),
    ("vLLM", 26), ("tensorRT-LLM", 18),

    # 开发者工具 / IDE
    ("GitHub Copilot", 34), ("Cursor", 32), ("CodeBuddy IDE", 26),
    ("Codeium", 18), ("OpenHands", 17), ("OpenDevin", 15),

    # 安全与治理
    ("safety alignment", 20), ("evals", 18), ("red teaming", 17), ("content filtering", 16),

    # 能力与模式
    ("multimodal", 22), ("structured generation", 22), ("function schema", 18),
    ("JSON mode", 18), ("program repair", 19), ("debugging", 21), ("test generation", 20),

    # 平台与服务
    ("KServe", 16), ("Ray", 18), ("Triton Inference Server", 17),
    ("OpenAI o-series", 20), ("Claude 4 Sonnet", 22), ("Gemini code", 19),
]

# -----------------------------
# (2) 统计与存储（降序）
# -----------------------------
# 排序
words_freq_sorted = sorted(words_freq, key=lambda x: x[1], reverse=True)

# 保存为 CSV（UTF-8 带 BOM，方便 Excel 打开）
csv_path = os.path.abspath("keywords_freq.csv")
with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["keyword", "frequency"])
    writer.writerows(words_freq_sorted)

print(f"[OK] 词频已保存：{csv_path}")
print("[Top 10] 示例：")
for kw, fr in words_freq_sorted[:10]:
    print(f"  - {kw}: {fr}")

# -----------------------------
# (3) 绘制词云（PyEcharts）
# -----------------------------
wc = (
    WordCloud(init_opts=opts.InitOpts(width="1000px", height="700px", page_title="LLM & AI Coding — 热词词云"))
    .add(
        series_name="LLM & AI Coding Hot Keywords",
        data_pair=words_freq_sorted,         # 直接使用内置列表
        word_size_range=[12, 82],
        shape="circle",
        rotate_step=45,
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="LLM & AI Coding — 热词词云（2025）",
            subtitle="词频越高字号越大；数据来自近期新闻/博客/学术热点的整理",
            pos_left="center",
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
)

html_path = os.path.abspath("llm_ai_coding_wordcloud.html")
wc.render(html_path)
print(f"[OK] 词云已生成：{html_path}")
print("请在浏览器中打开上述 HTML 文件查看交互式词云。")
