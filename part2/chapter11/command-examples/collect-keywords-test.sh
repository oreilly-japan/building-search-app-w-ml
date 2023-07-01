docker compose exec workspace \
    sh -c "cat hands_on_keywords.txt | awk 'NR==1,NR==500 {print}' > hands_on_keywords.txt.test"
