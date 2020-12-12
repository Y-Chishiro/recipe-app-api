FROM python:3.7-alpine
MAINTAINER Yusukec Ltd

# Python起動の際の推奨
ENV PYTHONUNBUFFERED 1

# カレントフォルダのファイルをコピーする
COPY ./requirements.txt /requirements.txt

# POSTGRESのdependenciesのインストール
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

# dependenciesのインストール
RUN pip install -r /requirements.txt

# POSTGRESQL系
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# セキュリティのため作成したユーザでの実行を推奨
# 通常だとroot権限のため、乗っ取られたときなんでもされてしまう。
RUN adduser -D user
USER user
