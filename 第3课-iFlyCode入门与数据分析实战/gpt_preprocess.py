# -*- coding: utf-8 -*-
"""
NSL-KDD 数据预处理脚本
功能：
1) 读取本地 KDDTrain+.txt / KDDTest+.txt，清理空白、统一标签，生成二分类标签(normal/attack)
2) protocol_type / service / flag -> One-Hot；其余数值特征 -> 标准化 与 归一化（分别输出两套数据）
3) 保证训练与测试经过相同变换且列顺序一致；保存特征名与标签
4) 打印样本数量、特征维度与标签分布（logging）

使用：
python prep_nslkdd.py  # 或将本文件内容保存后直接运行
"""

import os
import json
import logging
from typing import Tuple, List

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from joblib import dump

# --------------------- 基本配置 ---------------------
TRAIN_PATH = "KDDTrain+.txt"
TEST_PATH  = "KDDTest+.txt"
OUT_DIR    = "processed"

LOG_LEVEL = logging.INFO
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# KDD/NSL-KDD 列名（41特征 + label + difficulty）
COLUMNS = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent",
    "hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
    "count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"
]

CAT_COLS = ["protocol_type", "service", "flag"]
# 数值列 = 全部去掉类别列与 label
NUM_COLS = [c for c in COLUMNS if c not in CAT_COLS + ["label"]]

# 将原始 label 归并为二类标签
def to_binary_label(raw: pd.Series) -> pd.Series:
    raw2 = raw.astype(str).str.strip().str.lower()
    return np.where(raw2.eq("normal"), "normal", "attack")

def read_nslkdd(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, header=None, names=COLUMNS)
    # 去除字段两侧空白（特别是标签）
    for col in ["label", *CAT_COLS]:
        df[col] = df[col].astype(str).str.strip()
    return df

def build_pipelines() -> Tuple[Pipeline, Pipeline]:
    cat = OneHotEncoder(handle_unknown="ignore", sparse=False)
    std = ColumnTransformer(
        transformers=[
            ("cat", cat, CAT_COLS),
            ("num", StandardScaler(), NUM_COLS)
        ],
        remainder="drop"
    )
    mm = ColumnTransformer(
        transformers=[
            ("cat", cat, CAT_COLS),
            ("num", MinMaxScaler(feature_range=(0, 1)), NUM_COLS)
        ],
        remainder="drop"
    )
    return Pipeline([("pre", std)]), Pipeline([("pre", mm)])

def get_feature_names(ct: ColumnTransformer) -> List[str]:
    names = []
    for name, trans, cols in ct.transformers_:
        if name == "remainder" and trans == "drop":
            continue
        if hasattr(trans, "get_feature_names_out"):
            # OneHotEncoder / Scaler
            base = trans.get_feature_names_out(cols)
            names.extend(list(base))
        else:
            # 兜底
            names.extend(list(cols))
    return names

def describe_split(tag: str, y_bin: pd.Series):
    vc = y_bin.value_counts().sort_index()
    total = int(vc.sum())
    normal = int(vc.get("normal", 0))
    attack = int(vc.get("attack", 0))
    logging.info(
        f"[{tag}] samples={total}, normal={normal} ({normal/total:.2%}), "
        f"attack={attack} ({attack/total:.2%}), ratio attack:normal={attack/max(normal,1):.2f}"
    )

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # 1) 读取并清理
    logging.info("Reading datasets ...")
    df_train = read_nslkdd(TRAIN_PATH)
    df_test  = read_nslkdd(TEST_PATH)

    # 统一标签为二分类
    y_train = pd.Series(to_binary_label(df_train["label"]), name="label_binary")
    y_test  = pd.Series(to_binary_label(df_test["label"]),  name="label_binary")

    X_train = df_train.drop(columns=["label"])
    X_test  = df_test.drop(columns=["label"])

    # 2) 构建两套预处理（标准化 / 归一化），仅在训练集 fit
    pipe_std, pipe_mm = build_pipelines()
    logging.info("Fitting StandardScaler pipeline on train ...")
    X_train_std = pipe_std.fit_transform(X_train)
    X_test_std  = pipe_std.transform(X_test)

    logging.info("Fitting MinMaxScaler pipeline on train ...")
    X_train_mm = pipe_mm.fit_transform(X_train)
    X_test_mm  = pipe_mm.transform(X_test)

    # 特征名（与列顺序严格一致）
    feat_std = get_feature_names(pipe_std.named_steps["pre"])
    feat_mm  = get_feature_names(pipe_mm.named_steps["pre"])

    # 3) 保存数据与元信息
    logging.info("Saving processed outputs ...")
    np.savez_compressed(os.path.join(OUT_DIR, "X_train_std.npz"), X=X_train_std)
    np.savez_compressed(os.path.join(OUT_DIR, "X_test_std.npz"),  X=X_test_std)
    np.savez_compressed(os.path.join(OUT_DIR, "X_train_minmax.npz"), X=X_train_mm)
    np.savez_compressed(os.path.join(OUT_DIR, "X_test_minmax.npz"),  X=X_test_mm)

    y_train.to_csv(os.path.join(OUT_DIR, "y_train_binary.csv"), index=False)
    y_test.to_csv(os.path.join(OUT_DIR, "y_test_binary.csv"), index=False)

    with open(os.path.join(OUT_DIR, "features_std.json"), "w", encoding="utf-8") as f:
        json.dump(feat_std, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "features_minmax.json"), "w", encoding="utf-8") as f:
        json.dump(feat_mm, f, ensure_ascii=False, indent=2)

    # 保存预处理器，便于后续模型推理保持一致
    dump(pipe_std, os.path.join(OUT_DIR, "preprocess_std.joblib"))
    dump(pipe_mm,  os.path.join(OUT_DIR, "preprocess_minmax.joblib"))

    # 4) 日志统计
    describe_split("Train", y_train)
    describe_split("Test",  y_test)
    logging.info(f"Shapes | X_train_std={X_train_std.shape}, X_test_std={X_test_std.shape}")
    logging.info(f"Shapes | X_train_minmax={X_train_mm.shape}, X_test_minmax={X_test_mm.shape}")
    logging.info(f"Saved to: {os.path.abspath(OUT_DIR)}")

if __name__ == "__main__":
    main()
