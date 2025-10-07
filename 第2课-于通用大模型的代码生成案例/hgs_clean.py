import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# 读取数据
df = pd.read_csv('data.csv')

# 分离好评和差评
positive_reviews = df[df['label'] == '好评']['content']
negative_reviews = df[df['label'] == '差评']['content']

# 中文分词函数
def chinese_word_segmentation(texts):
    words_list = []
    for text in texts:
        # 去除标点符号和数字
        text = re.sub(r'[^\u4e00-\u9fa5]', ' ', str(text))
        # 使用jieba分词
        words = jieba.cut(text)
        # 过滤单字和空格
        words = [word for word in words if len(word) > 1]
        words_list.extend(words)
    return words_list

# 对好评和差评分别进行分词
positive_words = chinese_word_segmentation(positive_reviews)
negative_words = chinese_word_segmentation(negative_reviews)

# 统计词频
positive_word_freq = Counter(positive_words)
negative_word_freq = Counter(negative_words)

# 生成词云函数
def generate_word_cloud(word_freq, title, filename):
    # 设置中文字体，需要根据系统调整路径
    font_path = 'SimHei.ttf'  # 可以使用系统自带的中文字体，如SimHei.ttf
    
    wordcloud = WordCloud(
        font_path=font_path,
        width=800,
        height=600,
        background_color='white',
        max_words=100
    ).generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

# 生成好评词云图
generate_word_cloud(positive_word_freq, 'Good WordCloud', 'positive_wordcloud.png')

# 生成差评词云图
generate_word_cloud(negative_word_freq, 'Bad WordCloud', 'negative_wordcloud.png')

# 打印前20个高频词
print("好评前20个高频词:")
for word, count in positive_word_freq.most_common(20):
    print(f"{word}: {count}")

print("\n差评前20个高频词:")
for word, count in negative_word_freq.most_common(20):
    print(f"{word}: {count}")
