import pandas as pd
import jieba
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, MaxPooling1D, Bidirectional, LSTM, Dense, Dropout
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 1. 读取数据
data = pd.read_csv('data.csv')
texts = data['content'].values
labels = data['label'].values

# 2. 中文分词处理
def chinese_cut(text):
    return ' '.join(jieba.cut(text))

texts_cut = [chinese_cut(text) for text in texts]

# 3. 标签编码
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)
labels_categorical = to_categorical(labels_encoded)

# 4. 文本向量化
tokenizer = Tokenizer(num_words=5000)  # 限制词汇表大小
tokenizer.fit_on_texts(texts_cut)
sequences = tokenizer.texts_to_sequences(texts_cut)

# 5. 序列填充
max_length = 100  # 设置最大序列长度
X = pad_sequences(sequences, maxlen=max_length)

# 6. 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, labels_categorical, test_size=0.2, random_state=42
)

# 7. 构建CNN-BiLSTM模型
model = Sequential()
model.add(Embedding(input_dim=5000, output_dim=128, input_length=max_length))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Bidirectional(LSTM(64, return_sequences=True)))
model.add(Bidirectional(LSTM(32)))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))  # 二分类输出层

# 8. 编译模型
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# 9. 训练模型
history = model.fit(
    X_train, y_train,
    batch_size=32,
    epochs=10,
    validation_data=(X_test, y_test),
    verbose=1
)

# 10. 评估模型
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'测试集准确率: {accuracy:.4f}')
