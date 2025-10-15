# ===================================
# Step 1: 导入必要库
# ===================================
import matplotlib.pyplot as plt          # 绘图工具
from sklearn.datasets import load_iris # 加载内置数据集
from sklearn.model_selection import train_test_split  # 划分训练集/测试集
from sklearn.ensemble import RandomForestClassifier    # 随机森林算法
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix # 评估指标
import seaborn as sns                   # 高级热力图可视化
import numpy as np                     # 数值计算支持

# ===================================
# Step 2: 准备数据 - Iris是经典的多类别分类问题（3个类别）
# ===================================
iris = load_iris()                     # 自动下载数据集（特征+真实标签）
X = iris.data                          # 特征矩阵 (n_samples × n_features)
y = iris.target                        # 目标变量 (0/1/2代表三种花的种类)
feature_names = iris.feature_names     # ['sepal length', 'sepal width', ...]
target_names = iris.target_names        # ['setosa', 'versicolor', 'virginica']

# 按7:3比例分割训练集和测试集，保证结果可泛化
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ===================================
# Step 3: 创建并训练随机森林模型
# ===================================
rf_classifier = RandomForestClassifier(
    n_estimators=100,               # 决策树数量（越多通常效果越好但耗时更长）
    criterion='gini',              # 分裂标准：基尼不纯度（替代方案='entropy'信息增益）
    max_depth=None,                 # 不限制树深度以避免过拟合
    random_state=42                # 固定随机种子确保结果可复现
)
rf_classifier.fit(X_train, y_train)      # 在训练数据上拟合模型

# ===================================
# Step 4: 预测与性能评估
# ===================================
y_pred = rf_classifier.predict(X_test)   # 对测试集做推断
accuracy = accuracy_score(y_test, y_pred) # 计算准确率（正确预测的比例）
print(f"Test Accuracy: {accuracy:.4f}") # e.g. 0.9737 → 97.37%

# 打印详细的分类报告（精确率/召回率/F1分数按类别拆分）
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=target_names))

# 显示混淆矩阵（实际vs预测的交叉表）
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, cmap='Blues', fmt='d', xticklabels=target_names, yticklabels=target_names)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# ===================================
# Step 5: 特征重要性分析 & 可视化
# ===================================
importances = rf_classifier.feature_importances_  # 获取每个特征的贡献度评分
indices = np.argsort(importances)[::-1]             # 从高到低排序索引

plt.figure(figsize=(8, 6))
plt.barh(range(len(indices)), [importances[i] for i in indices], color='teal')
plt.yticks([i + 0.5 for i in range(len(indices))], [feature_names[i] for i in indices])
plt.xlabel('Relative Importance Score')
plt.title('Feature Importance Ranking by Random Forest')
plt.tight_layout()
plt.show()