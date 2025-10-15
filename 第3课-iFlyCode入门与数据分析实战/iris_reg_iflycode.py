#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# 1. 加载数据集并提取目标变量
iris = load_iris()
X = iris.data[:, 3].reshape(-1, 1)    # 花瓣宽度作为特征（第4列）
y = iris.data[:, 2]                   # 花瓣长度作为目标变量（第3列）
feature_name = iris.feature_names[3] # 'petal width (cm)'
target_name = iris.feature_names[2]   # 'petal length (cm)'

# 2. 划分训练集与测试集（7:3比例）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. 创建并训练线性回归模型
reg = LinearRegression()
reg.fit(X_train, y_train)

# 4. 进行预测并评估性能指标
y_pred = reg.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"均方误差(MSE): {mse:.4f}")
print(f"决定系数R2: {r2:.4f}")

# 5. 绘制结果可视化
plt.figure(figsize=(10, 6))

# 原始数据散点图
plt.scatter(X, y, color='blue', label='实际观测值', alpha=0.6)

# 回归线及置信区间阴影区域
sorted_idx = np.argsort(X.ravel())
sort_X = X[sorted_idx]
sort_yhat = reg.predict(sort_X)
plt.plot(sort_X, sort_yhat, color='red', linewidth=2, label='线性回归拟合线')
plt.fill_between(sort_X.ravel(), 
                 sort_yhat - np.std(y_train - reg.predict(X_train)),
                 sort_yhat + np.std(y_train - reg.predict(X_train)),
                 color='pink', alpha=0.2, label='±1标准差范围')

# 标注关键信息
coef = reg.coef_[0]
intercept = reg.intercept_
equation_text = f'y = {coef:.2f}x + {intercept:.2f}'
plt.annotate(equation_text, xy=(0.05, 0.85), xycoords='axes fraction',
             bbox=dict(facecolor='white', alpha=0.8))

# 图表美化设置
plt.title(f'花瓣宽度 vs 花瓣长度回归分析\n({feature_name} → {target_name})', fontsize=14)
plt.xlabel(feature_name, fontsize=12)
plt.ylabel(target_name, fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()