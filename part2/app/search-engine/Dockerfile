FROM docker.elastic.co/elasticsearch/elasticsearch:7.13.4

ADD https://github.com/o19s/elasticsearch-learning-to-rank/releases/download/v1.5.7-es7.13.4/ltr-plugin-v1.5.7-es7.13.4.zip /tmp/
RUN bin/elasticsearch-plugin install --batch file:///tmp/ltr-plugin-v1.5.7-es7.13.4.zip
RUN rm /tmp/ltr-plugin-v1.5.7-es7.13.4.zip
