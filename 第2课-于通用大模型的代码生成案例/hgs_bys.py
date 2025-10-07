import pandas as pd
import jieba
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix

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
tfidf = TfidfVectorizer()
X_train_tfidf = tfidf.fit_transform(X_train_cut)
X_test_tfidf = tfidf.transform(X_test_cut)

# 4. 构建朴素贝叶斯模型并进行训练预测
nb = MultinomialNB()
nb.fit(X_train_tfidf, y_train)
y_pred = nb.predict(X_test_tfidf)

# 5. 评估模型效果并输出结果
print("分类报告:")
print(classification_report(y_test, y_pred))

# 绘制混淆矩阵热力图
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['差评', '好评'], 
            yticklabels=['差评', '好评'])
plt.title('混淆矩阵热力图')
plt.ylabel('真实标签')
plt.xlabel('预测标签')
plt.tight_layout()
plt.savefig('confusion_matrix_heatmap.png')
plt.show()

# 输出模型准确率
accuracy = (y_pred == y_test).mean()
print(f"\n模型准确率: {accuracy:.4f}")
