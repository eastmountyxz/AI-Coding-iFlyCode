import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import logging
from typing import List

# ============== 日志 ==============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('preprocessing.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ============== 辅助函数 ==============
def clean_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

def unify_labels_binary(series: pd.Series) -> pd.Series:
    # NSL-KDD：除 normal 以外均视为 attack
    s = series.astype(str).str.strip().str.lower()
    return np.where(s.eq('normal'), 'normal', 'attack')

# ============== 主流程 ==============
class NSLKDDPreprocessor:
    def __init__(self):
        self.categorical_features = ['protocol_type', 'service', 'flag']
        self.numerical_features: List[str] = []  # 延后在读取数据后确定

    @staticmethod
    def get_expected_columns():
        # NSL-KDD/KDD+ 的标准 43 列（41 特征 + label + difficulty）
        return [
            "duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent",
            "hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root",
            "num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
            "count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
            "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
            "dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
            "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"
        ]

    def load_data(self, filepath: str) -> pd.DataFrame:
        try:
            # NSL-KDD 为**逗号分隔**，无表头
            df = pd.read_csv(filepath, sep=',', header=None, names=self.get_expected_columns(), engine='python')
            logger.info(f"成功加载文件: {filepath}  形状: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"加载文件失败 {filepath}: {e}")
            raise

    def preprocess(self, train_path: str, test_path: str):
        # ------- 读取 & 清理 -------
        df_train = clean_whitespace(self.load_data(train_path))
        df_test  = clean_whitespace(self.load_data(test_path))

        # 统一二分类标签
        df_train['label'] = unify_labels_binary(df_train['label'])
        df_test['label']  = unify_labels_binary(df_test['label'])

        # 拆分 X/y
        X_train = df_train.drop(columns=['label'])
        y_train = df_train['label']
        X_test  = df_test.drop(columns=['label'])
        y_test  = df_test['label']

        # 在读取后再确定数值列（此时 X_* 无 label）
        self.numerical_features = [c for c in X_train.columns if c not in self.categorical_features]

        # ------- 预处理器 -------
        # 兼容老版 sklearn：sparse=False
        cat_enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
        std_ct = ColumnTransformer(
            transformers=[
                ('cat', cat_enc, self.categorical_features),
                ('num', StandardScaler(), self.numerical_features),
            ],
            remainder='drop'
        )

        mm_ct = ColumnTransformer(
            transformers=[
                ('cat', cat_enc, self.categorical_features),
                ('num', MinMaxScaler((0, 1)), self.numerical_features),
            ],
            remainder='drop'
        )

        # 只在训练集 fit，测试集 transform
        logger.info("Fit/Transform 标准化版本 ...")
        X_train_std = std_ct.fit_transform(X_train)
        X_test_std  = std_ct.transform(X_test)

        logger.info("Fit/Transform 归一化版本 ...")
        X_train_mm = mm_ct.fit_transform(X_train)
        X_test_mm  = mm_ct.transform(X_test)

        # ------- 生成特征名（One-Hot 展开 + 数值列） -------
        def make_feature_names(ct: ColumnTransformer) -> List[str]:
            cat: OneHotEncoder = ct.named_transformers_['cat']
            cat_names = []
            for col, cats in zip(self.categorical_features, cat.categories_):
                cat_names += [f"{col}={c}" for c in cats]
            num_names = self.numerical_features
            return cat_names + num_names

        feat_std = make_feature_names(std_ct)
        feat_mm  = make_feature_names(mm_ct)

        # 转为 DataFrame 并附上标签
        train_std = pd.DataFrame(X_train_std, columns=feat_std)
        train_std['label'] = y_train.values
        test_std = pd.DataFrame(X_test_std, columns=feat_std)
        test_std['label'] = y_test.values

        train_mm = pd.DataFrame(X_train_mm, columns=feat_mm)
        train_mm['label'] = y_train.values
        test_mm = pd.DataFrame(X_test_mm, columns=feat_mm)
        test_mm['label'] = y_test.values

        # ------- 统计 -------
        self.log_stats(train_std, "训练集(标准化)")
        self.log_stats(test_std, "测试集(标准化)")
        self.log_stats(train_mm, "训练集(归一化)")
        self.log_stats(test_mm, "测试集(归一化)")

        return (train_std, test_std), (train_mm, test_mm)

    def log_stats(self, df: pd.DataFrame, name: str):
        logger.info(f"=== {name} ===")
        logger.info(f"样本数: {len(df)}, 特征维度(不含label): {df.shape[1]-1}")
        dist = df['label'].value_counts(normalize=True).rename(lambda x: f"{x}_ratio").round(4)
        cnt  = df['label'].value_counts().rename(lambda x: f"{x}_count")
        logger.info("标签分布:\n" + pd.concat([cnt, dist], axis=1).to_string())
        logger.info("前5行:\n" + df.head().to_string())

if __name__ == "__main__":
    processor = NSLKDDPreprocessor()
    train_file = "KDDTrain+.txt"
    test_file  = "KDDTest+.txt"

    try:
        (train_std, test_std), (train_mm, test_mm) = processor.preprocess(train_file, test_file)
        # 保存
        train_std.to_csv("processed_train_std.csv", index=False)
        test_std.to_csv("processed_test_std.csv", index=False)
        train_mm.to_csv("processed_train_minmax.csv", index=False)
        test_mm.to_csv("processed_test_minmax.csv", index=False)
        logger.info("预处理完成，已输出标准化与归一化两个版本。")
    except Exception as e:
        logger.critical(f"预处理过程中发生错误: {e}")
        raise
