import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. 加载数据集
iris = load_iris()
X = iris.data       # 特征矩阵 (150条样本 × 4个特征)
y = iris.target     # 真实标签 (0/1/2对应三种鸢尾花类别)
feature_names = iris.feature_names  # ['sepal length', 'sepal width', ...]

# 2. 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. 创建并训练随机森林模型
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 4. 预测与评估
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"准确率: {accuracy:.2f}")
print("\n混淆矩阵:")
print(confusion_matrix(y_test, y_pred))
print("\n分类报告:")
print(classification_report(y_test, y_pred))

# 5. 可视化决策边界（选择前两个特征）
plt.figure(figsize=(10, 6))
colors = ['r', 'g', 'b']  # 红、绿、蓝对应三个类别

# 绘制训练样本散点图
for i in range(3):
    idx = (y == i)
    plt.scatter(X[idx, 0], X[idx, 1], c=colors[i], label=f'类别 {i}', alpha=0.7, edgecolor='k')

# =====================================================
# 关键修正部分：构造包含所有4个特征的网格
# =====================================================
# 获取全局均值用于填充缺失的特征列
mean_values = np.mean(X, axis=0)

# 定义范围（仅针对前两个特征变化）
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))

# 构建完整输入矩阵：每一行形如 [sepal_length, sepal_width, petal_length_fixed, petal_width_fixed]
grid = np.column_stack([
    xx.ravel(),                 # 第一列：萼片长度（动态变化）
    yy.ravel(),                 # 第二列：萼片宽度（动态变化）
    np.full(xx.size, mean_values[2]),      # 第三列：花瓣长度设为全局均值
    np.full(xx.size, mean_values[3])       # 第四列：花瓣宽度设为全局均值
])

# 现在 grid 的形状是 (N, 4)，符合模型期望的输入格式
Z = rf.predict(grid).reshape(xx.shape)

# 绘制等高线和填充区域
plt.contourf(xx, yy, Z, alpha=0.4, levels=[0, 1, 2])
plt.contour(xx, yy, Z, colors=['k'], linestyles='--', linewidths=0.5)

# 添加图表装饰
plt.title('随机森林分类决策边界 (萼片长宽 vs 花瓣长宽)', fontsize=14)
plt.xlabel(feature_names[0], fontsize=12)
plt.ylabel(feature_names[1], fontsize=12)
plt.legend(loc='best', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()