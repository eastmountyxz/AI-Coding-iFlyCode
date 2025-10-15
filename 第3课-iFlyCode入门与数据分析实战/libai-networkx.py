import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import random

# =============================
# Part 1: 模拟李白相关人物数据 (实际应用应替换为真实文本挖掘结果)
# =============================
def generate_sample_data():
    """生成示例性的共现关系数据"""
    # 核心人物列表（包含李白本人）
    characters = ['李白', '杜甫', '孟浩然', '王维', '贺知章', '高适', '岑参', '王昌龄']
    
    # 创建加权共现字典 {人物A: {人物B: 权重, ...}, ...}
    cooccurrence = defaultdict(dict)
    
    # 随机生成连接强度（模拟文本中的共现频率）
    for i in range(len(characters)):
        for j in range(i+1, len(characters)):
            weight = random.uniform(0.5, 3.0)  # 随机权重代表亲密程度
            cooccurrence[characters[i]][characters[j]] = weight
            cooccurrence[characters[j]][characters[i]] = weight  # 无向图需双向添加
    
    return characters, cooccurrence

# =============================
# Part 2: 构建网络图结构
# =============================
def build_relationship_graph():
    """根据共现数据创建带权无向图"""
    G = nx.Graph()
    nodes, edges_data = generate_sample_data()
    
    # 添加节点并设置属性
    for node in nodes:
        G.add_node(node, label=node)
        # 根据度数动态调整节点大小（后续计算）
    
    # 添加带权重的边
    for source, targets in edges_data.items():
        for target, weight in targets.items():
            G.add_edge(source, target, weight=weight)
    
    return G

# =============================
# Part 3: 高级可视化设置
# =============================
def visualize_with_style(graph):
    """应用专业级的可视化样式"""
    plt.figure(figsize=(12, 8))
    
    # 基于PageRank算法确定节点重要性排序
    pagerank = nx.pagerank(graph)
    
    # 动态计算节点尺寸（基础值+PR加成）
    node_sizes = [v * 1500 + 300 for v in pagerank.values()]
    
    # 按权重设置边的粗细和透明度
    edge_widths = [d['weight'] * 2 for u, v, d in graph.edges(data=True)]
    edge_alphas = [min(0.9, d['weight']/3) for u, v, d in graph.edges(data=True)]
    
    # 使用spring布局算法（更适合社会关系网络）
    pos = nx.spring_layout(graph, k=0.3, iterations=50)  # k控制间距紧凑度
    
    # 绘制网络主体
    nx.draw_networkx_nodes(
        graph, pos,
        node_color='skyblue',
        node_shape='o',
        node_size=node_sizes,
        edgecolors='black',
        linewidths=2
    )
    
    nx.draw_networkx_edges(
        graph, pos,
        width=edge_widths,
        alpha=edge_alphas,
        edge_color='gray'
    )
    
    # 添加标签避让机制
    nx.draw_networkx_labels(
        graph, pos,
        font_size=12,
        font_family='SimHei',
        font_weight='bold',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
    )
    
    # 显示边权重注释
    edge_labels = {(u, v): f"{round(d['weight'],1)}" 
                   for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(
        graph, pos,
        edge_labels=edge_labels,
        label_pos=0.6,
        font_color='darkred',
        font_size=9
    )
    
    plt.title("李白社交关系图谱", fontsize=16, pad=20)
    plt.axis('off')  # 隐藏坐标轴
    plt.tight_layout()
    plt.show()

# =============================
# Part 4: 执行流程
# =============================
if __name__ == "__main__":
    try:
        # 初始化知识图谱
        poetry_graph = build_relationship_graph()
        
        # 输出基本统计信息供调试
        print(f"节点总数: {poetry_graph.number_of_nodes()}")
        print(f"关系总数: {poetry_graph.number_of_edges()}")
        print("\n度数中心性TOP3:")
        degrees = dict(poetry_graph.degree())
        sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:3]
        for char, deg in sorted_degrees:
            print(f"{char}: {deg}个连接")
        
        # 渲染可视化结果
        visualize_with_style(poetry_graph)
        
    except Exception as e:
        print(f"程序执行出错: {str(e)}")