docker compose exec workspace \
    sh -c "
    bzcat simplewiki-202109-pages-with-pageviews-20211001.bz2 |\
    cut -f2 |\
    shuf -n 4000 --random-source=simplewiki-202109-pages-with-pageviews-20211001.bz2 \
    > hands_on_keywords.txt
    "
