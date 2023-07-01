#!/usr/bin/env python
import bz2

from elasticsearch import Elasticsearch
from elasticsearch import helpers


def generate_bulk_buffer():
    buf = []
    with bz2.open("simplewiki-202109-pages-with-pageviews-20211001.bz2", "rt") as bz2f:
        for l in bz2f:
            id, title, text, pageviews = l.rstrip().split("\t")
            buf.append(
                {
                    "_op_type": "create",
                    "_index": "simplewiki",
                    "_id": id,
                    "_source": {
                        "title": title,
                        "text": text,
                        "pageviews": int(pageviews),
                    },
                }
            )
            if 500 <= len(buf):  # 500記事ずつバッファして返す
                yield buf
                buf.clear()

    if buf:  # 最後に端数の記事を返す
        yield buf


elasticsearch = Elasticsearch("http://search-engine:9200/")

for buf in generate_bulk_buffer():
    try:
        helpers.bulk(elasticsearch, buf, refresh="true")
    except Exception:
        pass  # ハンズオンのため、例外を無視する

elasticsearch.close()
