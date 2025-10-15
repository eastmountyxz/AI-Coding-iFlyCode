import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# (1) 读取数据
train_path = 'processed_train_std.csv'
test_path = 'processed_test_std.csv'

# 加载训练集和测试集
train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

# 分离特征与标签（假设最后一列是label）
X_train = train_df.iloc[:, :-1].values  # 所有行，除最后一列外的所有列作为特征
y_train = train_df['label'].values     # 最后一列为目标变量
X_test = test_df.iloc[:, :-1].values
y_test = test_df['label'].values

# (2) 训练模型 - 构建随机森林算法（n_estimators=11）
rf = RandomForestClassifier(n_estimators=11, random_state=42)
rf.fit(X_train, y_train)

# (3) 预测与评估
y_pred = rf.predict(X_test)

# 计算并绘制混淆矩阵
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=sorted(set(y_test)))
disp.plot(cmap=plt.cm.Blues)  # 使用蓝色调色板
plt.title('Confusion Matrix')
plt.show()

# 可选：打印分类报告获取更多指标细节
from sklearn.metrics import classification_report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))