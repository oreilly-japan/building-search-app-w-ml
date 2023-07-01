#!/usr/bin/env python

import warnings

from argparse import ArgumentParser
from elasticsearch import Elasticsearch

from es_query import (
    generate_query_to_search_with_default,
    generate_query_to_collect_features,
    generate_query_to_search_with_mlr,
)


def parse_response(response):
    titles = [d["_source"]["title"] for d in response["hits"]["hits"]]
    features = [
        d["fields"]["_ltrlog"][0]["log_entry0"] if "fields" in d else None
        for d in response["hits"]["hits"]
    ]
    hits = response["hits"]["total"]["value"]
    took = response["took"]
    return titles, features, hits, took


parser = ArgumentParser()
parser.add_argument("target", choices=["baseline", "feature", "mlr"])
parser.add_argument("output_path")
parser.add_argument("keywords_path")
parser.add_argument("--window-size", type=int, default=100)
parser.add_argument("--extract-hits-and-took", action="store_true")
args = parser.parse_args()

args.output_group_path = args.output_path + ".group"

# ハンズオンなので、DeprecationWarningを無効にしてコンソールを見やすくする
warnings.filterwarnings("ignore", category=DeprecationWarning)

extra_query_params = {}
if args.target == "baseline":
    generate_query_func = generate_query_to_search_with_default
elif args.target == "feature":
    generate_query_func = generate_query_to_collect_features
elif args.target == "mlr":
    generate_query_func = generate_query_to_search_with_mlr
    extra_query_params["window_size"] = args.window_size
else:
    raise ValueError(f"Unknown target: {args.target}")

es = Elasticsearch("http://search-engine:9200/")

with open(args.keywords_path) as f, open(args.output_path, "w") as of, open(
    args.output_group_path, "w"
) as gf:
    for keywords in f:
        keywords = keywords.strip()
        body = generate_query_func(keywords, **extra_query_params)
        try:
            response = es.search(index="simplewiki", body=body)
            titles, features, hits, took = parse_response(response)
            labels = [int(title == keywords) for title in titles]
            # target == featureのとき、label種類が2つ以上あるリクエストのみを結果に出力する
            if args.target == "feature" and len(set(labels)) < 2:
                continue
            # --extract-hits-and-tookが指定されているとき: hitsとtookを空白区切りで出力する
            # それ以外: labelとfeature情報（レスポンスに存在する場合のみ）を空白区切りで出力する
            if args.extract_hits_and_took:
                of.write(f"{hits} {took}\n")
            else:
                for label, feature in zip(labels, features):
                    tokens = []
                    tokens.append(str(label))
                    if feature is not None:
                        for i, f in enumerate(feature):
                            tokens.append(f"{i}:{f['value']}")
                    of.write(f"{' '.join(tokens)}\n")
            gf.write(f"{len(titles)}\n")
        except Exception:
            continue  # ハンズオンなので何かしらで例外が発生した場合は無視する
