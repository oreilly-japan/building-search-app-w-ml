import os

import pandas as pd
import streamlit as st
from elasticsearch import Elasticsearch

from es_query import (
    generate_query_to_search_with_default,
    generate_query_to_search_with_mlr,
)


# streamlit UIオプション設定
st.set_page_config(layout="wide")

# 接続先Elasticsearch
elasticsearch_url = os.environ["ELASTICSEARCH_HOSTS"]
es = Elasticsearch(elasticsearch_url)

# 検索キーワード
keywords = st.text_input(label="Please input search keywords.", value="")

# 検索キーワードが空ならば、処理を打ち切る
if not keywords:
    st.stop()

# Elasticsearchに検索リクエストを送る
default_query = generate_query_to_search_with_default(keywords, size=20)
default_result = es.search(index="simplewiki", **default_query)["hits"]["hits"]
mlr_query = generate_query_to_search_with_mlr(keywords, size=20)
mlr_result = es.search(index="simplewiki", **mlr_query)["hits"]["hits"]

# 左列: Elasticsearchデフォルトスコアによるランキング
# 右列: 検索ランキングモデルによるランキング
default_col, mlr_col = st.columns(2)

# 検索レスポンスに含まれる文書のタイトルおよびスコアを表示

with default_col:
    st.header("default")
    st.table(
        pd.DataFrame(
            {
                "title": [h["_source"]["title"] for h in default_result],
                "score": [h["_score"] for h in default_result],
            }
        )
    )

with mlr_col:
    st.header("ranking model")
    st.table(
        pd.DataFrame(
            {
                "title": [h["_source"]["title"] for h in mlr_result],
                "score": [h["_score"] for h in mlr_result],
            }
        )
    )
