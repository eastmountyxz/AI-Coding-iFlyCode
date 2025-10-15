import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

# =============================
# (1) 读取CSV并预处理数据
# =============================
def load_data(train_path, test_path):
    # 加载训练集和测试集
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    # 分离特征与标签（假设最后一列为label）
    X_train = train_df.iloc[:, :-1].values.astype('float32')  # 确保数值类型
    y_train = train_df['label'].map({'normal': 0, 'attack': 1}).values  # 映射为0/1
    X_test = test_df.iloc[:, :-1].values.astype('float32')
    y_test = test_df['label'].map({'normal': 0, 'attack': 1}).values
    
    # Reshape成(samples, features, 1)格式以适配CNN输入
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    
    return X_train, y_train, X_test, y_test

# =============================
# (2) 构建CNN-BiLSTM混合模型
# =============================
def build_model(input_shape):
    model = Sequential()
    # CNN部分 - 提取局部特征
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.5))
    
    # BiLSTM部分 - 捕捉双向时序依赖关系
    model.add(Bidirectional(LSTM(units=128, return_sequences=False)))
    model.add(Dropout(0.5))
    
    # 全连接层输出二分类结果
    model.add(Dense(1, activation='sigmoid'))
    
    # 编译模型
    model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])
    return model

# =============================
# (3) 评估与可视化
# =============================
def evaluate_model(model, X_test, y_test):
    # 预测概率和类别
    y_pred_proba = model.predict(X_test)
    y_pred = (y_pred_proba > 0.5).astype(int)
    
    # 计算指标
    acc = model.evaluate(X_test, y_test)[1]
    print(f"Test Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # 混淆矩阵处理
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Normal', 'Attack'])
    disp.plot(cmap=plt.cm.Blues)
    plt.title('Confusion Matrix Heatmap')
    plt.show()

# =============================
# 主程序流程
# =============================
if __name__ == "__main__":
    # 文件路径设置（根据实际情况修改）
    train_file = 'processed_train_std.csv'
    test_file = 'processed_test_std.csv'
    
    # 加载数据
    X_train, y_train, X_test, y_test = load_data(train_file, test_file)
    input_shape = X_train.shape[1:]  # (features, channels)
    
    # 创建模型
    model = build_model(input_shape)
    model.summary()  # 打印模型结构
    
    # 训练模型
    history = model.fit(X_train, y_train, batch_size=32, epochs=5, validation_split=0.2)
    
    # 评估结果
    evaluate_model(model, X_test, y_test)