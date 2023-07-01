#!/usr/bin/env python

import json

from xgboost import DMatrix, train


# featuresetから特徴量名を取得する
def get_feature_names_from_featureset():
    with open("hands_on_featureset.json") as featureset_fp:
        featureset = json.load(featureset_fp)
        feature_names = [e["name"] for e in featureset["featureset"]["features"]]
    return feature_names


feature_names = get_feature_names_from_featureset()


# XGBoost学習パラメータ
params = {
    "objective": "rank:pairwise",
    "eval_metric": "ndcg",
    "tree_method": "hist",
    "grow_policy": "lossguide",
    "max_leaves": 60,
    "subsample": 0.45,
    "eta": 0.1,
    "seed": 0,
}


# 訓練データセット
training_input = DMatrix(
    "hands_on_featuredata.txt.training", feature_names=feature_names
)

# 検証データセット
validation_input = DMatrix(
    "hands_on_featuredata.txt.validation", feature_names=feature_names
)

# モデルの学習
evals = [(training_input, "train"), (validation_input, "valid")]
bst = train(
    params,
    training_input,
    num_boost_round=200,
    evals=evals,
    verbose_eval=10,
)

# モデルの出力
model = bst.get_dump(dump_format="json")

with open("hands_on_model.json", "w") as f:
    wrapped_model = {
        "model": {
            "name": "hands_on_model.json",
            "model": {
                "type": "model/xgboost+json",
                "definition": "[" + ",".join(list(model)) + "]",
            },
        }
    }
    json.dump(wrapped_model, f, indent=2)
    f.write("\n")
