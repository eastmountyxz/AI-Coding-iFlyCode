import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ===================================
# Step 1: 加载数据 & 预处理
# ===================================
iris = load_iris()          # 内置标准数据集
X = iris.data               # 特征矩阵 (已归一化过? → 我们显式标准化更安全)
feature_names = iris.feature_names   # ['sepal length', 'sepal width', ...]

# 关键预处理：标准化特征使各维度权重均衡
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ===================================
# Step 2: 执行 KMeans 聚类 (k=3)
# ===================================
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
cluster_labels = kmeans.fit_predict(X_scaled)
centroids = kmeans.cluster_centers_  # 获取三个簇的中心点坐标(在标准化后的空间中)

# 将中心点反转换回原始尺度以便绘图解释
centroids_original_space = scaler.inverse_transform(centroids)

# ===================================
# Step 3: 可视化设置
# ===================================
plt.figure(figsize=(10, 6))
colors = ['tab:red', 'tab:blue', 'tab:green']  # 不同簇的颜色区分
markers = ['o', 's', '^']                     # 圆形/方形/三角形表示不同簇
larger_dot_size = 150                         # 突出显示中心点的尺寸

# 绘制每个样本点 + 对应颜色的标记
for i in range(3):
    # 提取属于当前簇的所有样本索引
    mask = cluster_labels == i
    plt.scatter(X[mask, 0], X[mask, 1], c=colors[i], label=f'Cluster {i+1}', alpha=0.7, edgecolors='w')
    # 绘制该簇的中心点 (用更大且空心的符号)
    plt.scatter([centroids_original_space[i][0]], [centroids_original_space[i][1]], 
                c='black', marker=markers[i], s=larger_dot_size, facecolors='none', linewidth=2, zorder=5)

# ===================================
# Step 4: 美化图表元素
# ===================================
plt.xlabel(feature_names[0])      # x轴标签: Sepal length (cm)
plt.ylabel(feature_names[1])      # y轴标签: Sepal width (cm)
plt.title('KMeans Clustering on Iris Data', fontsize=14)
plt.legend(loc='best')            # 自动选择最佳位置放置图例
plt.grid(linestyle='--', alpha=0.3) # 添加虚线网格辅助观察
plt.tight_layout()                # 防止标签被截断
plt.show()