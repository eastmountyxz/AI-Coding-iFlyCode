import pandas as pd
import jieba
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from matplotlib import font_manager as fm

# ============================
# 简化版中文字体解决方案（仅使用微软雅黑）
# ============================
def setup_chinese_fonts():
    """自动配置微软雅黑字体环境"""
    # Windows系统路径
    font_path = r'C:\Windows\Fonts\msyh.ttc'
    
    if os.path.exists(font_path):
        try:
            # 创建FontProperties对象
            prop = fm.FontProperties(fname=font_path)
            prop.set_size(14)  # 设置字号
            plt.rcParams['font.family'] = prop.get_name()
            plt.rcParams['axes.unicode_minus'] = False  # 确保负号正常显示
            print("成功加载微软雅黑字体")
            return prop
        except Exception as e:
            print(f"加载失败: {str(e)}")
    
    raise RuntimeError("未找到微软雅黑字体！请检查路径是否正确或手动指定其他中文字体。")

# 获取字体属性
chinese_font = setup_chinese_fonts()

# ============================
# ① 数据读取：生成样本并写入CSV
# ============================
def generate_sample_data():
    data = [
        {"诗题": "静夜思", "作者": "李白", "朝代": "唐", "诗句": "床前明月光，疑是地上霜。举头望明月，低头思故乡。"},
        {"诗题": "春晓", "作者": "孟浩然", "朝代": "唐", "诗句": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。"},
        {"诗题": "登鹳雀楼", "作者": "王之涣", "朝代": "唐", "诗句": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。"},
        {"诗题": "赋得古原草送别", "作者": "白居易", "朝代": "唐", "诗句": "离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。"}
    ]
    df = pd.DataFrame(data)
    df.to_csv("TangPoems.csv", index=False, encoding='utf-8-sig')
    return df

# ============================
# ② 文本处理：中文分词+去停用词
# ============================
def preprocess_text(text, stopwords_set):
    words = list(jieba.cut(text))
    filtered = [w for w in words if w not in stopwords_set and len(w) > 1]
    return filtered

BASE_STOPWORDS = {"的", "了", "在", "是", "和", "与", "及", "着", "过", "到", "着", "啊", "呀", "呢", "吗", "吧", "啦"}

# ============================
# ③ 实体识别：抽取关键元素
# ============================
def extract_entities(row):
    entities = {}
    entities["作者"] = row["作者"]
    entities["朝代"] = row["朝代"]
    entities["诗题"] = row["诗题"]
    sentence = row["诗句"]
    tokens = preprocess_text(sentence, BASE_STOPWORDS)
    imagery_keywords = ["月", "鸟", "花", "草", "山", "河", "风", "雨", "雪"]
    entities["意象"] = list(set([t for t in tokens if t in imagery_keywords]))
    positive_cues = ["明", "荣", "生", "上"]
    negative_cues = ["霜", "落", "烧", "枯"]
    sentiment = "积极" if any(p in tokens for p in positive_cues) else "消极"
    entities["情感"] = sentiment
    return entities

# ============================
# ④ 关系抽取：建立三元组连接
# ============================
def build_triplets(entities_list):
    triplets = []
    for entity in entities_list:
        triplets.append((entity["作者"], "创作", entity["诗题"]))
        triplets.append((entity["诗题"], "属于", entity["朝代"]))
        for imge in entity["意象"]:
            triplets.append((entity["诗题"], "包含", imge))
        triplets.append((entity["诗题"], "表达", entity["情感"]))
    return triplets

# ============================
# ⑤ 知识图谱构建与可视化（最终修复版）
# ============================
def visualize_kg(triplets):
    G = nx.DiGraph()
    for h, r, t in triplets:
        G.add_edge(h, t, label=r)
    
    pos = nx.spring_layout(G, seed=42)
    num_nodes = len(G.nodes())
    colors = plt.cm.tab20(np.linspace(0, 1, num_nodes))
    
    fig, ax = plt.subplots(figsize=(16, 10))  # 增大画布尺寸以获得更好的布局
    
    # 绘制节点（无文字内容）
    nx.draw_networkx_nodes(G, pos, node_size=2500, node_color=colors, ax=ax)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=30, edge_color='lightgray', width=2, ax=ax)
    
    # 正确设置中文字体的方法：使用FontProperties对象
    nx.draw_networkx_labels(G, pos, font_size=14, ax=ax)
    
    # 添加关系标注
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, ax=ax)
    
    # 优化显示效果
    ax.set_facecolor('whitesmoke')  # 设置背景色使对比更明显
    ax.grid(False)                 # 移除网格线
    plt.tight_layout()             # 自动调整子图参数
    plt.savefig("TangPoem_KG.png", dpi=300, bbox_inches='tight')  # 确保保存时不留白边
    plt.close()

# ============================
# 主执行流程
# ============================
if __name__ == "__main__":
    df = generate_sample_data()
    all_entities = [extract_entities(row) for _, row in df.iterrows()]
    triplets = build_triplets(all_entities)
    triplet_df = pd.DataFrame(triplets, columns=["head", "relation", "tail"])
    triplet_df.to_csv("TangPoem_KG.csv", index=False, encoding='utf-8-sig')
    visualize_kg(triplets)
    
    print("\n任务完成！已生成以下文件：")
    print("TangPoems.csv      → 原始诗歌数据")
    print("TangPoem_KG.csv    → 结构化三元组知识库")
    print("TangPoem_KG.png    → 知识图谱可视化图像")
