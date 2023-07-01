FROM python:3.7

RUN pip install matplotlib xgboost scikit-learn elasticsearch~=7.17

# TODO: 正式な配布場所が決まったらパスを変更する
ADD redistribution/simplewiki-202109-pages-with-pageviews-20211001.bz2 .

COPY workspace/ .
COPY es_query.py .
