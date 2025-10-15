import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_iris
import numpy as np

# Step 1: Load built-in Iris dataset & select relevant features/target
iris = load_iris()
X = iris.data[:, 3].reshape(-1, 1)      # Petal width (feature) → Reshape for SKLearn input
y = iris.data[:, 2]                     # Petal length (target variable)
feature_names = ['Petal Width (cm)', 'Petal Length (cm)']

# Step 2: Train linear regression model
# 创建一个线性回归模型实例
model = LinearRegression()
# 使用特征矩阵X和目标向量y来训练（拟合）模型
model.fit(X, y)
# 格式化输出截距和斜率，保留四位小数
coefficients = f"Intercept={model.intercept_:.4f}, Slope={model.coef_[0]:.4f}"

# Step 3: Create prediction range for smooth line plotting
x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_pred = model.predict(x_range)

# Step 4: Visualization with raw data points + regression line
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X[:, 0], y=y, alpha=0.7, label='Observed Data')
plt.plot(x_range, y_pred, color='red', linewidth=2, label=f'Fitted Line: {coefficients}')
plt.title('Linear Regression: Predicting Petal Length from Petal Width', fontsize=12)
plt.xlabel(feature_names[0])
plt.ylabel(feature_names[1])
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()