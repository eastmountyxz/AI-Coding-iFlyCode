import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# =============================
# (1) 读取数据
# =============================
train_df = pd.read_csv('processed_train_std.csv')
test_df = pd.read_csv('processed_test_std.csv')

# 分离特征和标签（假设最后一列为label）
X_train = train_df.iloc[:, :-1].values      # 所有行，除最后一列外的所有列作为特征
y_train = train_df.iloc[:, -1].values        # 最后一列作为目标变量
X_test = test_df.iloc[:, :-1].values         # 同上处理测试集
y_test = test_df.iloc[:, -1].values

# =============================
# (2) 构建SVM模型并训练
# =============================
# 创建带RBF核的支持向量机分类器
# C: 正则化参数控制容错率(越大越严格拟合训练数据)，gamma影响单个样本的影响范围
clf = svm.SVC(kernel='rbf', C=10, gamma='scale')  # 'scale'自动适配特征方差倒数
clf.fit(X_train, y_train)                     # 用训练集拟合模型

# =============================
# (3) 预测与评估
# =============================
y_pred = clf.predict(X_test)                  # 对测试集进行预测
cm = confusion_matrix(y_test, y_pred)          # 计算混淆矩阵原始数值

# 可视化混淆矩阵（带归一化的百分比标注）
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y_test))
disp.plot(cmap=plt.cm.Blues)                   # 使用蓝色系热力图样式
plt.title('Normalized Confusion Matrix (Test Set)')
plt.xticks(rotation=45)                        # 旋转x轴标签防止重叠
plt.show()

# 可选：输出分类报告获取更多指标细节
from sklearn.metrics import classification_report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))