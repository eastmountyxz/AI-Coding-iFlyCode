import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

# ============================
# Step 1: 模拟共现数据 (替换为您的真实数据)
cooccurrence_data = {
    "李白": [("杜甫", 5), ("王维", 8), ("孟浩然", 7), ("黄鹤楼", 3), ("长安", 6)],
    "杜甫": [("李白", 5), ("高适", 4), ("严武", 2)],
    "王维": [("李白", 8), ("孟浩然", 9), ("终南山", 4)],
    "孟浩然": [("李白", 7), ("王维", 9), ("襄阳", 5)],
    "黄鹤楼": [("李白", 3), ("崔颢", 2)],
    "长安": [("李白", 6), ("玄宗", 3)],
    "高适": [("杜甫", 4)],
    "严武": [("杜甫", 2)],
    "终南山": [("王维", 4)],
    "襄阳": [("孟浩然", 5)],
    "崔颢": [("黄鹤楼", 2)],
    "玄宗": [("长安", 3)]
}

# ============================
# Step 2: 构建图结构
G = nx.Graph()

entities = set()
for entity, connections in cooccurrence_data.items():
    entities.add(entity)
    for neighbor, _ in connections:
        entities.add(neighbor)

for entity in entities:
    G.add_node(entity)

for entity, connections in cooccurrence_data.items():
    for neighbor, weight in connections:
        if G.has_edge(entity, neighbor):
            G[entity][neighbor]['weight'] += weight
        else:
            G.add_edge(entity, neighbor, weight=weight)

# ============================
# Step 3: 可视化配置
plt.figure(figsize=(12, 8))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码

degree = dict(G.degree())
pos = nx.spring_layout(G, seed=42)  # 固定布局种子保证可复现

# 绘制边（按权重设置透明度）
edges = G.edges(data=True)
for edge in edges:
    nx.draw_networkx_edges(
        G, pos,
        edgelist=[edge],
        width=edge[2]['weight'] * 0.5,
        alpha=0.7,
        edge_color='gray'
    )

# 绘制节点（大小与度数成正比）
nx.draw_networkx_nodes(
    G, pos,
    node_size=[v * 300 for v in degree.values()],
    node_color='skyblue',
    edgecolors='black',
    linewidths=1
)

# 添加节点标签（关键修改：移除 label_pos 参数）
nx.draw_networkx_labels(
    G, pos,
    font_size=10,
    font_family='SimHei',
    font_weight='bold'
)

# 添加标题并关闭坐标轴
plt.title("李白人物关系共现图谱", fontsize=14, pad=20)
plt.axis('off')

# ============================
# Step 4: 显示图形
plt.tight_layout()
plt.show()
