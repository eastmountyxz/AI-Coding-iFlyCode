import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def create_libai_relationship_graph():
    """创建李白人物关系图"""
    # 直接定义共现次数 (人物: 与李白共现的次数)
    cooccurrence_data = {
        '杜甫': 15,
        '孟浩然': 12,
        '王维': 9,
        '贺知章': 8,
        '高适': 7,
        '岑参': 6,
        '王昌龄': 5,
        '白居易': 4,
        '元稹': 3,
        '贾岛': 2,
        '柳宗元': 2,
        '韩愈': 1
    }
    
    # 创建空图
    G = nx.Graph()
    
    # 添加中心节点(李白)
    G.add_node('李白', size=3000, color='gold')
    
    # 根据共现次数添加其他节点和边
    for person, count in cooccurrence_data.items():
        # 添加节点属性
        G.add_node(person, size=1000 + count*200)
        # 添加带权重的边
        G.add_edge('李白', person, weight=count)
    
    return G

def visualize_graph(G):
    """可视化图形"""
    plt.figure(figsize=(12, 8))
    
    # 获取节点位置 (使用spring布局算法)
    pos = nx.spring_layout(G, k=0.3, iterations=50)
    
    # 提取边的权重用于设置线条粗细
    edge_weights = [d['weight'] for u, v, d in G.edges(data=True)]
    
    # 绘制边
    nx.draw_networkx_edges(
        G, pos, width=edge_weights, edge_color='gray', alpha=0.7
    )
    
    # 绘制节点 - 根据与李白的关系强度着色
    colors = ['gold'] + ['lightblue'] * (len(G) - 1)
    nx.draw_networkx_nodes(
        G, pos, node_size=[n[1]['size'] for n in G.nodes(data=True)],
        node_color=colors, alpha=0.9
    )
    
    # 添加标签
    nx.draw_networkx_labels(
        G, pos, font_size=12, font_family='SimHei', font_weight='bold'
    )
    
    # 添加标题和说明
    plt.title("李白人物关系共现网络图", fontsize=16, pad=20)
    plt.axis('off')  # 关闭坐标轴
    
    # 添加图例解释颜色含义
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='gold', label='李白'),
        Patch(facecolor='lightblue', label='其他诗人'),
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 创建关系图
    relationship_graph = create_libai_relationship_graph()
    
    # 可视化展示
    visualize_graph(relationship_graph)