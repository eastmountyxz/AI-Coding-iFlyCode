# 导入所需库
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from matplotlib import rcParams

# 设置中文字体为 SimHei（黑体），解决负号显示异常
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# 1. 加载 Iris 数据集（来自 scikit-learn）
from sklearn.datasets import load_iris
iris = load_iris()
df = pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                  columns=iris['feature_names'] + ['species'])

# &#9888;️ 关键修改：使用真实的列名（含空格和单位）
X = df[['petal width (cm)']].values    # 特征矩阵（二维）
y = df['petal length (cm)'].values     # 目标向量

# 3. 创建并训练线性回归模型
model = LinearRegression()
model.fit(X, y)

# 4. 使用模型进行预测
y_pred = model.predict(X)

# 5. 绘制散点图 + 回归线
plt.figure(figsize=(8, 6))
plt.scatter(X, y, color='blue', label='实际数据点')
plt.plot(X, y_pred, color='red', linewidth=2, label='回归线')

# 添加标题和标签
plt.title('花瓣宽度 vs 花瓣长度 - 线性回归拟合', fontsize=14)
plt.xlabel('花瓣宽度 (cm)', fontsize=12)
plt.ylabel('花瓣长度 (cm)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 6. 输出模型性能指标
print(f"回归方程: petal_length = {model.intercept_:.4f} + {model.coef_[0]:.4f} × petal_width")
print(f"决定系数 R² = {r2_score(y, y_pred):.4f}")
