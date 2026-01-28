import pandas as pd
import jieba
from jieba import analyse
import random
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple

# ===================================
# 配置参数区（可根据需要调整）
# ===================================
RANDOM_SEED = 42          # 固定随机种子保证结果可复现
NUM_SAMPLES = 10          # 生成的唐诗样本数量
OUTPUT_TRIPLE_FILE = "TangPoem_KG.csv"      # 三元组输出文件名
OUTPUT_IMAGE_FILE = "TangPoem_KG.png"        # 知识图谱图片文件名

# 预定义资源库
AUTHORS = ["李白", "杜甫", "王维", "白居易", "李商隐", "杜牧", "孟浩然"]
DYNASTIES = ["唐"] * len(AUTHORS)           # 所有作者都属于唐朝
POETRY_TITLES = [
    "《静夜思》", "《春晓》", "《登鹳雀楼》", "《赋得古原草送别》", 
    "《相思》", "《江雪》", "《寻隐者不遇》", "《枫桥夜泊》",
    "《游子吟》", "《早发白帝城》"
]
CLASSICAL_LINES = [
    "床前明月光，疑是地上霜",          # 李白《静夜思》
    "春眠不觉晓，处处闻啼鸟",          # 孟浩然《春晓》
    "白日依山尽，黄河入海流",          # 王之涣《登鹳雀楼》（注：虽非本列表作者但借用名句）
    "离离原上草，一岁一枯荣",          # 白居易《赋得古原草送别》
    "红豆生南国，春来发几枝",          # 王维《相思》
    "千山鸟飞绝，万径人踪灭",          # 柳宗元《江雪》（补充经典意象）
    "松下问童子，言师采药去",          # 贾岛《寻隐者不遇》
    "月落乌啼霜满天，江枫渔火对愁眠",  # 张继《枫桥夜泊》
    "慈母手中线，游子身上衣",          # 孟郊《游子吟》
    "朝辞白帝彩云间，千里江陵一日还"   # 李白《早发白帝城》
]

IMAGERY_DICT = {               # 常见诗歌意象词典
    "明月": ["月", "月光"],
    "清风": ["风", "微风"],
    "雁": ["大雁", "鸿雁"],
    "霜": ["秋霜", "寒霜"],
    "柳": ["杨柳", "垂柳"],
    "花": ["花朵", "鲜花"],
    "雨": ["细雨", "春雨"],
    "雪": ["白雪", "积雪"],
    "山": ["高山", "青山"],
    "水": ["流水", "河水"]
}

SENTIMENT_INDICATORS = {       # 情感指示词映射表
    "正面": ["喜", "乐", "欢", "笑", "悦", "兴"],
    "负面": ["悲", "愁", "泪", "恨", "忧", "哀"]
}

# ===================================
# 辅助函数集合
# ===================================
def set_randomness():
    """设置全局随机状态以确保结果可复现"""
    random.seed(RANDOM_SEED)

def generate_sample_dataset() -> pd.DataFrame:
    """生成模拟用的唐诗数据集"""
    data = []
    for i in range(NUM_SAMPLES):
        author = random.choice(AUTHORS)
        dynasty = DYNASTIES[AUTHORS.index(author)]
        title = random.choice(POETRY_TITLES)
        line = random.choice(CLASSICAL_LINES)
        data.append({
            "诗题": title,
            "作者": author,
            "朝代": dynasty,
            "诗句": line
        })
    return pd.DataFrame(data)

def load_stopwords() -> set:
    """加载中文停用词表（简化版）"""
    return {"的", "了", "和", "与", "及", "着", "在", "是", "有", "我", "你", "他", "她", "它"}

def tokenize_text(text: str, stopwords: set) -> List[str]:
    """执行中文分词并过滤停用词"""
    words = jieba.lcut(text)                # 精确模式分词
    filtered = [w for w in words if w not in stopwords and len(w) > 1]
    return filtered

def extract_entities(row: pd.Series, stopwords: set) -> Dict:
    """从单条记录中提取关键实体信息"""
    content = row["诗句"]
    tokens = tokenize_text(content, stopwords)
    
    # 1. 提取意象实体（基于预定义词典匹配）
    imagery_set = set()
    for base_word in IMAGERY_DICT:
        variants = IMAGERY_DICT[base_word]
        matched = any(variant in tokens for variant in variants)
        if matched:
            imagery_set.add(base_word)
    
    # 2. 判断情感倾向（基于情感词汇统计）
    pos_score = sum(tokens.count(w) for w in SENTIMENT_INDICATORS["正面"])
    neg_score = sum(tokens.count(w) for w in SENTIMENT_INDICATORS["负面"])
    sentiment = "正面" if pos_score > neg_score else "负面"
    
    return {
        "title": row["诗题"],
        "author": row["作者"],
        "dynasty": row["朝代"],
        "imagery": list(imagery_set),
        "sentiment": sentiment
    }

def extract_relations(entities: List[Dict]) -> List[Tuple[str, str, str]]:
    """根据解析出的实体生成标准化三元组关系"""
    triples = []
    for ent in entities:
        # 关系1: 作者 → 创作 → 诗题
        triples.append((ent["author"], "创作", ent["title"]))
        
        # 关系2: 诗题 → 属于 → 朝代
        triples.append((ent["title"], "属于", ent["dynasty"]))
        
        # 关系3: 诗题 → 包含 → 意象 (每个意象单独成一条记录)
        for im in ent["imagery"]:
            triples.append((ent["title"], "包含", im))
        
        # 关系4: 诗题 → 表达 → 情感
        triples.append((ent["title"], "表达", ent["sentiment"]))
    return triples

def build_knowledge_graph(triples: List[Tuple]) -> nx.DiGraph:
    """使用NetworkX构建有向知识图谱"""
    G = nx.DiGraph(name="唐诗知识图谱")
    
    # 批量添加带属性的边
    for head, rel, tail in triples:
        G.add_edge(head, tail, relation=rel)
    
    return G

def visualize_graph(graph: nx.DiGraph()):
    """渲染并保存知识图谱可视化结果"""
    plt.figure(figsize=(16, 12))
    
    # 使用力导向布局算法优化节点位置
    pos = nx.spring_layout(graph, k=0.8, iterations=80)
    
    # 绘制节点（按类型着色）
    node_colors = ['lightblue' if n.startswith('李白') else 'lightgreen' for n in graph.nodes()]
    nx.draw_networkx_nodes(graph, pos, node_size=800, node_color=node_colors)
    
    # 绘制带箭头的边
    nx.draw_networkx_edges(graph, pos, edge_color='gray', arrowstyle='->', arrowsize=20)
    
    # 添加标签文字
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family='SimHei')
    
    # 显示关系类型标注
    edge_labels = {(u, v): f"{d['relation']}" for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    
    plt.axis('off')             # 隐藏坐标轴
    plt.tight_layout()          # 自动调整布局防止重叠
    plt.savefig(OUTPUT_IMAGE_FILE, dpi=300)
    print(f"知识图谱已保存至 {OUTPUT_IMAGE_FILE}")

# ===================================
# 主执行流程
# ===================================
if __name__ == "__main__":
    # 初始化环境设置
    set_randomness()
    stopwords = load_stopwords()
    
    # =====> ① 数据读取模块 <=====
    df = generate_sample_dataset()
    print(" 数据集生成完成：")
    print(df.to_string(index=False))
    
    # =====> ② 文本处理模块 <=====
    processed_lines = df.apply(lambda r: tokenize_text(r["诗句"], stopwords), axis=1)
    print("\n 示例分词结果：")
    print(processed_lines.iloc[:2])
    
    # =====> ③ 实体识别模块 <=====
    entities = df.apply(lambda r: extract_entities(r, stopwords), axis=1).tolist()
    print("\n 提取到的实体信息：")
    for i, ent in enumerate(entities[:min(3, len(entities))]):
        print(f"样本#{i+1}: {ent}")
    
    # =====> ④ 关系抽取模块 <=====
    triples = extract_relations(entities)
    print("\n 生成的关系三元组：")
    for triple in triples[:min(5, len(triples))]:
        print(triple)
    
    # 保存三元组到CSV文件
    pd.DataFrame(triples, columns=["head", "relation", "tail"]).to_csv(
        OUTPUT_TRIPLE_FILE, index=False, encoding="utf-8"
    )
    print(f"\n 三元组已保存至 {OUTPUT_TRIPLE_FILE}")
    
    # =====> ⑤ 知识图谱构建与可视化 <=====
    kg = build_knowledge_graph(triples)
    visualize_graph(kg)