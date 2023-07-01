docker compose exec workspace \
    curl -X POST -w '\n' -H 'Content-Type: application/json' \
        -d @hands_on_featureset.json \
        "http://search-engine:9200/_ltr/_featureset/hands_on_featureset.json"
