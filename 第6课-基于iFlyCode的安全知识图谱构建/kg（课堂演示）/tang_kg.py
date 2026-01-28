import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import matplotlib.pyplot as plt
import jieba
import re
import os

# ----------------------
# 模块①: 数据读取与生成
# ----------------------
def generate_sample_data(file_path='tang_poems.csv'):
    """生成模拟唐诗数据集并写入CSV文件"""
    sample_data = [
        {'诗题': '静夜思', '作者': '李白', '朝代': '唐朝', '诗句': '床前明月光，疑是地上霜。举头望明月，低头思故乡。'},
        {'诗题': '春晓', '作者': '孟浩然', '朝代': '唐朝', '诗句': '春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。'},
        {'诗题': '登鹳雀楼', '作者': '王之涣', '朝代': '唐朝', '诗句': '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。'},
        {'诗题': '相思', '作者': '王维', '朝代': '唐朝', '诗句': '红豆生南国，春来发几枝。愿君多采撷，此物最相思。'},
        {'诗题': '江雪', '作者': '柳宗元', '朝代': '唐朝', '诗句': '千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。'}
    ]
    df = pd.DataFrame(sample_data)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"样本数据已生成至 {os.path.abspath(file_path)}")

# ----------------------
# 模块②: 文本处理工具
# ----------------------
class TextProcessor:
    def __init__(self):
        # 中文停用词列表（精简版）
        self.stopwords = set([
            '的', '地', '得', '着', '了', '过', '在', '有', '从', '向', '对', '关于',
            '而', '且', '与', '并', '或', '但', '却', '因', '为', '由于', '所以', '因此',
            '之', '其', '此', '这', '那', '哪', '谁', '何', '如何', '怎样', '多少', '几',
            '啊', '呀', '吧', '呢', '吗', '哦', '嗯', '哎', '喂', '嘿', '哟', '嗬', '啦', '呀', '哇', '哪'
        ])
        # 导入自定义词典（增强分词准确性）
        jieba.load_userdict('custom_dict.txt') if os.path.exists('custom_dict.txt') else None

    def segment(self, text):
        """中文分词"""
        return list(jieba.cut(text))

    def remove_stopwords(self, words):
        """去除停用词"""
        return [word for word in words if word not in self.stopwords and len(word) > 1]

# ----------------------
# 模块③: 实体识别模块
# ----------------------
class EntityRecognizer:
    def __init__(self, processor):
        self.processor = processor
        # 预定义实体类型及关键词映射
        self.entity_patterns = {
            '诗人': ['李白', '杜甫', '王维', '孟浩然', '王之涣', '柳宗元', '白居易', '李商隐', '杜牧'],
            '朝代': ['唐朝', '宋代', '元代', '明代', '清代'],
            '意象': ['明月', '春风', '花', '鸟', '山', '河', '雪', '红豆', '雨', '风', '楼', '舟', '翁'],
            '情感': ['思念', '孤独', '喜悦', '悲伤', '豁达', '惆怅', '寂寞', '向往']
        }

    def recognize_entities(self, row):
        """从单条诗歌记录中识别实体"""
        entities = {
            '诗题': [row['诗题']],
            '作者': [row['作者']],
            '朝代': [row['朝代']]
        }
        # 处理诗句文本
        poem_lines = row['诗句'].replace('，', '').replace('。', '')
        words = self.processor.segment(poem_lines)
        filtered_words = self.processor.remove_stopwords(words)
        
        # 匹配意象和情感
        for word in filtered_words:
            for etype, patterns in self.entity_patterns.items():
                if word in patterns:
                    if etype not in entities:
                        entities[etype] = []
                    if word not in entities[etype]:
                        entities[etype].append(word)
        return entities

# ----------------------
# 模块④: 关系抽取模块
# ----------------------
def extract_relations(entities):
    """根据实体信息抽取三元组关系"""
    relations = []
    # 作者-创作->诗题
    for author in entities.get('作者', []):
        for title in entities.get('诗题', []):
            relations.append((author, '创作', title))
    # 诗题-属于->朝代
    for title in entities.get('诗题', []):
        for dynasty in entities.get('朝代', []):
            relations.append((title, '属于', dynasty))
    # 诗题-包含->意象
    for title in entities.get('诗题', []):
        for image in entities.get('意象', []):
            relations.append((title, '包含', image))
    # 诗题-表达->情感
    for title in entities.get('诗题', []):
        for emotion in entities.get('情感', []):
            relations.append((title, '表达', emotion))
    return relations

# ----------------------
# 模块⑤: 知识图谱构建与可视化
# ----------------------
def build_and_visualize_kg(relations, output_image='TangPoem_KG.png'):
    """构建知识图谱并导出可视化图片"""
    G = nx.DiGraph()
    # 添加三元组到图中
    for head, rel, tail in relations:
        G.add_edge(head, tail, relation=rel)
    
    # 绘制图形
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=0.6, iterations=50)  # 布局参数调整
    
    # 节点标签样式设置
    node_labels = {n: f"{n}\n({G.in_degree(n)}入度)" for n in G.nodes()}
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2500, alpha=0.9)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_family='SimHei')
    
    # 边标签样式设置
    edge_labels = {(u, v): d['relation'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', width=1.5, arrowstyle='->', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=9)
    
    plt.title("唐诗知识图谱 (Tang Poetry Knowledge Graph)", fontsize=16, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"知识图谱已保存为 {os.path.abspath(output_image)}")
    plt.show()
    return G

# ----------------------
# 主函数执行流程
# ----------------------
def main():
    # 步骤1：生成并加载数据
    data_file = 'tang_poems.csv'
    generate_sample_data(data_file)
    df = pd.read_csv(data_file)
    
    # 初始化处理器和识别器
    processor = TextProcessor()
    recognizer = EntityRecognizer(processor)
    
    # 步骤2-3：处理每条诗歌记录
    all_relations = []
    for _, row in df.iterrows():
        entities = recognizer.recognize_entities(row)
        relations = extract_relations(entities)
        all_relations.extend(relations)
    
    # 步骤4：保存三元组到CSV
    kg_df = pd.DataFrame(all_relations, columns=['Head', 'Relation', 'Tail'])
    kg_df.to_csv('TangPoem_KG.csv', index=False, encoding='utf-8-sig')
    print(f"三元组已保存至 {os.path.abspath('TangPoem_KG.csv')}")
    
    # 步骤5：构建并可视化图谱
    build_and_visualize_kg(all_relations)

if __name__ == "__main__":
    main()
