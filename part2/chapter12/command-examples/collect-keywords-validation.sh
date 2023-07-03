docker compose exec workspace \
    sh -c "cat hands_on_keywords.txt | awk 'NR==3501,NR==4000 {print}' > hands_on_keywords.txt.validation"
