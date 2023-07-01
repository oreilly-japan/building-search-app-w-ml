docker compose exec workspace \
    sh -c "cat hands_on_keywords.txt | awk 'NR==501,NR==3500 {print}' > hands_on_keywords.txt.training"
