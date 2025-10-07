import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体防止乱码
plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载内置的鸢尾花数据集
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target
print("数据集前5行:")
print(df.head())

# 选取花瓣宽度作为自变量 X，花瓣长度作为因变量 y
X = df[['petal width (cm)']].values  # 注意转为二维数组
y = df['petal length (cm)'].values

print(f"样本数量: {len(X)}")
print(f"X均值±标准差: {np.mean(X):.2f} ± {np.std(X):.2f}")
print(f"y均值±标准差: {np.mean(y):.2f} ± {np.std(y):.2f}")


# 创建并训练线性回归模型
lr = LinearRegression()
lr.fit(X, y)

# 输出回归方程参数
print("\n回归方程: y = {:.2f} * x + {:.2f}".format(
    lr.coef_[0], lr.intercept_))
print(f"决定系数 R²: {lr.score(X, y):.4f}")

# 生成平滑的预测曲线用的X值
x_plot = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_pred = lr.predict(x_plot)

# 绘制散点图 + 回归线
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X.ravel(), y=y, alpha=0.7, color='blue', label='真实数据')
plt.plot(x_plot, y_pred, color='red', linewidth=2, label='回归线')

# 添加文本标注
plt.title('花瓣宽度 vs 花瓣长度的线性回归', fontsize=14)
plt.xlabel('花瓣宽度 (cm)', fontsize=12)
plt.ylabel('花瓣长度 (cm)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

