import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import pandas as pd

# 加载数据集
iris = load_iris()
X = iris.data       # 特征矩阵 (150×4)
y = iris.target     # 目标标签 (0,1,2对应三种花型)
feature_names = iris.feature_names   # ['sepal length', 'sepal width', 'petal length', 'petal width']
target_names = iris.target_names      # ['setosa', 'versicolor', 'virginica']

# 标准化数据（均值为0，标准差为1）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 创建DataFrame便于绘图
df = pd.DataFrame(X_scaled, columns=feature_names)
df['species'] = [target_names[i] for i in y]

# =============================
# 图1：类别分布图（柱状图+计数）
plt.figure(figsize=(8, 6))
ax1 = sns.countplot(x='species', data=df, palette="viridis")
ax1.set_title('各类别的样本数量分布', fontsize=14)
ax1.set_xlabel('物种类型', fontsize=12)
ax1.set_ylabel('数量', fontsize=12)
plt.show()

# =============================
# 图2：特征间的相关性热力图
plt.figure(figsize=(8, 6))
corr = df.corr()              # 计算相关系数矩阵
mask = np.triu(np.ones_like(corr)) # 只显示下三角部分避免重复展示
sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0,
            square=True, linewidths=0.5, annot_kws={"size": 10},
            xticklabels=feature_names, yticklabels=feature_names)
plt.title('标准化后的特征相关性热力图', fontsize=14)
plt.tight_layout()
plt.show()
