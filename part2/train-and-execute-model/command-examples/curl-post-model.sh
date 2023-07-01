docker compose exec workspace \
    curl -X POST -w '\n' -H 'Content-Type: application/json' -d @hands_on_model.json \
        "http://search-engine:9200/_ltr/_featureset/hands_on_featureset.json/_createmodel"
