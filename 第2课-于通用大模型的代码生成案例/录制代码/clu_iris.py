import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体防止乱码
plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载鸢尾花数据集
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target  # 添加真实类别标签（可选）
print("数据集前5行:")
print(df.head())

X = df[['petal length (cm)', 'petal width (cm)']].values

# 初始化 KMeans 模型 (k=3)
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

# 获取聚类结果
labels = kmeans.labels_          # 每个样本的簇标签
centers = kmeans.cluster_centers_  # 三个簇的中心点坐标

plt.figure(figsize=(10, 6))

# 绘制散点图（按聚类结果着色）
sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels, palette='viridis', 
                legend='brief', alpha=0.8, edgecolor='w')

# 绘制簇中心点（红色五角星）
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='d', 
            s=200, label='簇中心', edgecolor='k')

# 添加文本标注
plt.title('KMeans 聚类结果 (基于花瓣长度 & 宽度)', fontsize=14)
plt.xlabel('花瓣长度 (cm)', fontsize=12)
plt.ylabel('花瓣宽度 (cm)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
