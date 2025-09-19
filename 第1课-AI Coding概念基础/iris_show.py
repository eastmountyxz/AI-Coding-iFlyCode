import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import pandas as pd
import numpy as np

# 加载鸢尾花数据集
iris = load_iris()
df = pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])

# 标准化数值型特征（排除目标变量列）
features = iris['feature_names']
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])

# ================= 1. 类别分布图（小提琴图+箱线图组合） =================
plt.figure(figsize=(12, 6))
# 为每个特征创建子图，按类别着色
for i, col in enumerate(features):
    plt.subplot(1, len(features), i+1)
    sns.violinplot(x='target', y=col, data=df, inner="box", palette="Set2")
    plt.title(f'{col} by Species')
plt.suptitle('标准化后不同品种的特征分布 (Violin + Boxplots)', y=1.05)
plt.tight_layout()
plt.show()

# ================= 2. 特征相关性热力图 =================
# 计算相关系数矩阵
corr_matrix = df[features].corr()

# 创建遮罩避免重复显示上三角区域
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', vmin=-1, vmax=1,
            center=0, square=True, linewidths=0.5, linecolor='white',
            annot_kws={"size": 9})
plt.title('标准化后特征间的皮尔逊相关系数热力图')
plt.show()