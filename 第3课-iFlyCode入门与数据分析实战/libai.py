import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import random

def create_sample_data():
    """创建模拟的李白相关文本数据"""
    sentences = [
        "李白与杜甫同游泰山",
        "李白拜访孟浩然于鹿门山",
        "王维常与李白饮酒作诗",
        "李白和贺知章一见如故",
        "高适曾随李白远行塞外",
        "李白欣赏岑参的边塞诗风",
        "杜甫思念李白写下多首赠友诗",
        "孟浩然回赠李白新酿美酒",
        "王维邀李白共赏终南山色",
        "贺知章推荐李白入朝为官",
        "高适与李白论剑谈兵法",
        "岑参与李白畅谈西域见闻",
        "李白醉卧长安街头遇贺知章",
        "杜甫梦中见到李白挥毫泼墨",
        "孟浩然送别李白于江畔",
        "王维弹琴伴李白吟诵",
        "贺知章读李白新作大加赞赏",
        "高适陪李白策马驰骋草原",
        "岑参向李白请教诗歌技巧"
    ]
    return sentences

def extract_names(text):
    """简单提取中文人名（实际应用中应使用更复杂的NER模型）"""
    # 已知的可能的人名列表
    known_names = ['李白', '杜甫', '孟浩然', '王维', '贺知章', '高适', '岑参']
    return [name for name in known_names if name in text]

def build_cooccurrence_graph(sentences):
    """构建共现关系图"""
    G = nx.Graph()
    cooccurrence_counts = defaultdict(int)
    
    # 首先添加所有独特的节点
    all_names = set()
    for sent in sentences:
        names_in_sent = extract_names(sent)
        all_names.update(names_in_sent)
    
    for name in all_names:
        G.add_node(name, size=1000)  # 初始化节点属性
    
    # 统计共现次数
    for sent in sentences:
        names_in_sent = extract_names(sent)
        for i in range(len(names_in_sent)):
            for j in range(i+1, len(names_in_sent)):
                u, v = sorted((names_in_sent[i], names_in_sent[j]))
                cooccurrence_counts[(u, v)] += 1
    
    # 添加带权重的边
    for (u, v), count in cooccurrence_counts.items():
        G.add_edge(u, v, weight=count)
    
    return G

def visualize_graph(G):
    """可视化图形"""
    plt.figure(figsize=(12, 8))
    
    # 根据度数设置节点大小
    degrees = dict(G.degree())
    max_deg = max(degrees.values())
    node_sizes = [degrees[n] * 300 / max_deg for n in G.nodes()]
    
    # 根据权重设置边宽
    edge_widths = [d['weight'] * 2 for u, v, d in G.edges(data=True)]
    
    pos = nx.spring_layout(G, k=0.5, iterations=50)  # 使用弹簧算法布局
    
    # 绘制边
    nx.draw_networkx_edges(
        G, pos, width=edge_widths, edge_color='gray', alpha=0.7
    )
    
    # 绘制节点
    nx.draw_networkx_nodes(
        G, pos, node_size=node_sizes, node_color='lightblue', alpha=0.9
    )
    
    # 添加标签
    nx.draw_networkx_labels(
        G, pos, font_size=12, font_family='SimHei'
    )
    
    # 突出显示中心节点（李白）
    central_node = '李白'
    nx.draw_networkx_nodes(
        G, {central_node: pos[central_node]}, 
        node_size=node_sizes[list(G.nodes()).index(central_node)]*1.5,
        node_color='red', alpha=1.0
    )
    
    plt.title("李白人物关系共现网络图", fontsize=16)
    plt.axis('off')  # 关闭坐标轴
    plt.tight_layout()
    plt.show()

# 主程序
if __name__ == "__main__":
    # 获取数据
    sentences = create_sample_data()
    
    # 构建图
    cooccurrence_graph = build_cooccurrence_graph(sentences)
    
    # 可视化
    visualize_graph(cooccurrence_graph)