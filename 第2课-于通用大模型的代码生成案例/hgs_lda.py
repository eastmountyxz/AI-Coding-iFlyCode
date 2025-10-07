import pandas as pd
import jieba
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# 1. 读取CSV文件并随机划分
data = pd.read_csv('data.csv')
X = data['content']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. 使用Jieba进行中文分词
def chinese_cut(text):
    return ' '.join(jieba.cut(text))

X_train_cut = X_train.apply(chinese_cut)
X_test_cut = X_test.apply(chinese_cut)

# 3. 构建TF-IDF向量器并转换文本
tfidf = TfidfVectorizer(max_features=1000)  # 限制特征数量以便LDA处理
X_train_tfidf = tfidf.fit_transform(X_train_cut)

# 4. 构建LDA模型进行主题特征词挖掘
n_topics = 2  # 假设挖掘2个主题
lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
lda.fit(X_train_tfidf)

# 输出每个主题的特征词
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = f"主题 {topic_idx + 1}: "
        message += ", ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)

n_top_words = 20  # 每个主题显示前20个特征词
tfidf_feature_names = tfidf.get_feature_names_out()
print_top_words(lda, tfidf_feature_names, n_top_words)
