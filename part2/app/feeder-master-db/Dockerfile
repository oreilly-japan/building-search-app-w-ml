FROM python:3.7
RUN pip install elasticsearch

WORKDIR /app

# TODO: 正式な配布場所が決まったらパスを変更する
ADD redistribution/simplewiki-202109-pages-with-pageviews-20211001.bz2 .

COPY feeder-master-db/ .
