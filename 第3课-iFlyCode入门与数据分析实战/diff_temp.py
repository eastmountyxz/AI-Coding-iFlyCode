# 导入必要库
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. 加载数据集
iris = load_iris()
X = iris.data       # 特征矩阵 (150条样本 × 4个特征)
feature_names = iris.feature_names  # ['sepal length', 'sepal width', ...]

# 2. 数据标准化（关键步骤！消除量纲影响）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. 构建并训练KMeans模型
# 创建KMeans实例，设置聚类数量为3，启用Elbow方法自动确定最佳簇数，固定随机种子以保证结果可复现
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
# 对标准化后的数据进行拟合和预测，得到每个样本所属的簇标签（转为整型）
clusters = kmeans.fit_predict(X_scaled).astype(int)  # 显式转为整数
# 提取最终确定的三个簇的中心点坐标并按特征重要性排序
centroids = kmeans.cluster_centers_  # 获取簇中心坐标


# 4. 可视化 - 选择两个特征维度作图
plt.figure(figsize=(10, 6))
colors = ['r', 'g', 'b']  # 红绿蓝三色对应三个簇
markers = ['o', '^', 's']  # 圆形/三角形/方形表示数据点
centroid_markers = ['*', 'D', 'P']  # 星形/菱形/倒三角表示中心点

# 遍历每个簇进行绘图
for i in range(3):
    # 提取当前簇的数据点
    mask = clusters == i
    plt.scatter(
        X_scaled[mask, 2],  # 使用第3个特征 "petal length"
        X_scaled[mask, 3],  # 使用第4个特征 "petal width"
        c=colors[i],
        marker=markers[i],
        label=f'Cluster {i+1}',
        alpha=0.7,
        edgecolors='black'
    )
    # 绘制簇中心点
    plt.scatter(
        centroids[i][2],
        centroids[i][3],
        c='black',
        marker=centroid_markers[i],
        s=200,
        linewidth=2,
        label=f'Center {i+1}'
    )

# 5. 添加图表装饰
# 定义统一的字体大小变量
FONT_SIZE_TITLE = 14
FONT_SIZE_LABEL = 12
FONT_SIZE_LEGEND = 10

# 设置图表标题，明确展示的内容
plt.title('KMeans聚类结果 (花瓣长度 vs 花瓣宽度)', fontsize=FONT_SIZE_TITLE)
# 设置x轴标签为具体的“花瓣长度”
plt.xlabel('花瓣长度', fontsize=FONT_SIZE_LABEL)
# 设置y轴标签为具体的“花瓣宽度”
plt.ylabel('花瓣宽度', fontsize=FONT_SIZE_LABEL)
# 显示图例，并手动指定其位置在图表右上角外部
plt.legend(loc='upper right', fontsize=FONT_SIZE_LEGEND)
# 添加网格线，使用虚线样式并降低透明度以增强可读性
plt.grid(True, linestyle='--', alpha=0.3)
# 自动调整子图参数以避免重叠
plt.tight_layout()
# 显示绘制好的图表
plt.show()
