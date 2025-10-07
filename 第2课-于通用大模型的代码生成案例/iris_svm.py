# 导入必要库
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, classification_report, 
                             confusion_matrix, ConfusionMatrixDisplay)
from matplotlib.colors import ListedColormap

# 1. 加载并准备数据
iris = datasets.load_iris()
X = iris.data[:, :2]  # 仅使用前两个特征（萼片长宽）便于可视化
y = iris.target
feature_names = iris.feature_names[:2]  # ['sepal length', 'sepal width']

# 数据标准化（关键步骤！）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集/测试集
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

# 2. 训练SVM模型（线性核）
svm_clf = SVC(kernel='linear', C=1.0, decision_function_shape='ovr')
svm_clf.fit(X_train, y_train)

# 3. 预测与评估
y_pred = svm_clf.predict(X_test)
print(f"&#128269; 测试集准确率: {accuracy_score(y_test, y_pred):.2f}")
print("\n&#128203; 分类报告:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))
print("\n&#128260; 混淆矩阵:")
print(confusion_matrix(y_test, y_pred))

# 4. 可视化决策边界
def plot_decision_boundary(model, X, y, title):
    # 创建网格点用于绘制决策边界
    h = .02 * np.ones((X.shape[0], 1))  # 步长控制分辨率
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h[0]),
                         np.arange(y_min, y_max, h[0]))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # 绘制决策边界和样本点
    plt.figure(figsize=(10, 6))
    cmap = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])  # 红绿蓝对应三类
    plt.contourf(xx, yy, Z, alpha=0.4, cmap=cmap)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolor='k', s=50, cmap=cmap)
    
    # 标记支持向量
    sv = svm_clf.support_vectors_
    plt.scatter(sv[:, 0], sv[:, 1], s=100, facecolors='none', 
                edgecolors='black', label='Support Vectors')
    
    plt.title(title, fontsize=14)
    plt.xlabel(feature_names[0], fontsize=12)
    plt.ylabel(feature_names[1], fontsize=12)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

# 调用可视化函数
plot_decision_boundary(svm_clf, X_scaled, y, "SVM")
