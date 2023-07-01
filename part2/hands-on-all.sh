#!/bin/bash -ex

export COMPOSE_FILE=app/docker-compose.yml

# 記事検索システムの構成と起動

## 検索システムを立ち上げる

docker compose up -d

# ElasticsearchにWikipediaデータセットを保存する

## Elasticsearchにデータセットの内容を保存する

docker compose exec feeder-master-db ./feed_dump_to_elasticsearch.py

# ベースラインのランキングロジックを評価する

## ハンズオンにおけるランキングロジックのオフライン評価

### ベースラインのランキングロジックのオフライン評価

#### テスト用検索キーワードセットの収集

docker compose exec workspace \
    sh -c "
    bzcat simplewiki-202109-pages-with-pageviews-20211001.bz2 |\
    cut -f2 |\
    shuf -n 4000 --random-source=simplewiki-202109-pages-with-pageviews-20211001.bz2 \
    > hands_on_keywords.txt
    "

docker compose exec workspace \
    sh -c "cat hands_on_keywords.txt | awk 'NR==1,NR==500 {print}' > hands_on_keywords.txt.test"

#### ランキング結果の取得と関連度の付与

docker compose exec workspace \
    ./collect_responses.py baseline baseline.txt hands_on_keywords.txt.test

#### 評価指標の計算

docker compose exec workspace ./calc_ndcg.py baseline.txt

# 訓練データセットの生成

## featuresetのデプロイ

docker compose exec workspace curl -X PUT -w '\n' "http://search-engine:9200/_ltr"

docker compose exec workspace \
    curl -X POST -w '\n' -H 'Content-Type: application/json' \
        -d @hands_on_featureset.json \
        "http://search-engine:9200/_ltr/_featureset/hands_on_featureset.json"

## 訓練および検証用検索キーワードの収集

docker compose exec workspace \
    sh -c "cat hands_on_keywords.txt | awk 'NR==501,NR==3500 {print}' > hands_on_keywords.txt.training"

docker compose exec workspace \
    sh -c "cat hands_on_keywords.txt | awk 'NR==3501,NR==4000 {print}' > hands_on_keywords.txt.validation"

## 訓練および検証用検索キーワードの収集

docker compose exec workspace \
    ./collect_responses.py feature hands_on_featuredata.txt.training hands_on_keywords.txt.training

docker compose exec workspace \
    ./collect_responses.py feature hands_on_featuredata.txt.validation hands_on_keywords.txt.validation

# 検索ランキングモデルの学習と実行

## 検索ランキングモデルの学習

docker compose exec workspace ./generate_model.py

## 検索ランキングモデルのデプロイ

docker compose exec workspace \
    curl -X POST -w '\n' -H 'Content-Type: application/json' -d @hands_on_model.json \
        "http://search-engine:9200/_ltr/_featureset/hands_on_featureset.json/_createmodel"

## 検索ランキングモデルのランキング結果の収集

docker compose exec workspace \
    ./collect_responses.py mlr mlr.txt hands_on_keywords.txt.test

## 検索ランキングモデルのオフライン評価

docker compose exec workspace ./calc_ndcg.py mlr.txt

# 検索ランキングモデルによる性能影響の測定

## 検索ランキングモデルをオンオフしてレイテンシを比較

docker compose exec workspace \
    ./collect_responses.py baseline --extract-hits-and-took benchmark-baseline.txt hands_on_keywords.txt.test

docker compose exec workspace ./calc_took.py benchmark-baseline.txt

docker compose exec workspace \
    ./collect_responses.py mlr --extract-hits-and-took benchmark-mlr.txt hands_on_keywords.txt.test

docker compose exec workspace ./calc_took.py benchmark-mlr.txt

## ヒット件数とレイテンシの同時測定

docker compose exec workspace \
    ./scatter_plot.py benchmark-mlr.txt scatter-mlr.png

docker compose cp workspace:scatter-mlr.png .
