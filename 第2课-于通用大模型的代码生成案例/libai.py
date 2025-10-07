import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

# ======================
# 模拟数据：李白及相关人物的共现次数
# 格式: {(人物A, 人物B): 共现次数}
# ======================
cooccurrence_data = {
    ('李白', '杜甫'): 5,
    ('李白', '孟浩然'): 4,
    ('李白', '王维'): 3,
    ('李白', '王昌龄'): 3,
    ('李白', '高适'): 2,
    ('李白', '岑参'): 2,
    ('杜甫', '孟浩然'): 1,
    ('孟浩然', '王维'): 2,
    ('王维', '王昌龄'): 1,
    ('王昌龄', '高适'): 1,
    ('高适', '岑参'): 1
}

# ======================
# 创建图对象
G = nx.Graph()

# 添加带权重的边
for (u, v), weight in cooccurrence_data.items():
    G.add_edge(u, v, weight=weight)

# ======================
# 计算节点度数（用于设置节点大小）
degrees = dict(G.degree())
max_degree = max(degrees.values()) if degrees else 1

# ======================
# 绘制图形
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # 固定布局种子保证可复现

# 绘制边（按权重设置透明度）
edges = G.edges(data=True)
for u, v, data in edges:
    weight = data['weight']
    alpha = min(0.9, weight / max(cooccurrence_data.values()))  # 归一化透明度
    nx.draw_networkx_edges(
        G, pos, edgelist=[(u, v)], width=weight*0.8, alpha=alpha, edge_color='gray'
    )

# 绘制节点（按度数设置大小）
node_sizes = [degrees[n] * 300 for n in G.nodes()]
nx.draw_networkx_nodes(
    G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.9
)

# 添加标签
nx.draw_networkx_labels(
    G, pos, font_size=10, font_family='simhei', font_weight='bold'
)

# 添加标题和图例
plt.title("李白人物关系共现图谱", fontsize=16, pad=20)
plt.axis('off')  # 关闭坐标轴

# 显示图形
plt.tight_layout()
plt.show()
