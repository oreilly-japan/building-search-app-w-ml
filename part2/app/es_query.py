def generate_query_to_search_with_default(keywords, size=10):
    return {
        "query": {"match": {"text": keywords}},
        "size": size,
        "_source": ["title"],
    }


def generate_query_to_collect_features(keywords, size=10):
    return {
        "query": {"match": {"text": keywords}},
        "rescore": {
            "query": {
                "rescore_query": {
                    "sltr": {
                        "params": {"keywords": keywords},
                        "featureset": "hands_on_featureset.json",
                    }
                },
                "rescore_query_weight": 0.0,
            },
            "window_size": size,
        },
        "size": size,
        "_source": ["title"],
        "ext": {"ltr_log": {"log_specs": {"name": "log_entry0", "rescore_index": 0}}},
    }


def generate_query_to_search_with_mlr(keywords, size=10, window_size=100):
    return {
        "query": {"match": {"text": keywords}},
        "rescore": {
            "query": {
                "rescore_query": {
                    "sltr": {
                        "params": {"keywords": keywords},
                        "model": "hands_on_model.json",
                    }
                },
                "query_weight": 0.0,
            },
            "window_size": window_size,
        },
        "size": size,
        "_source": ["title"],
    }
