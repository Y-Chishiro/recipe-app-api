FROM python:3.9-alpine
MAINTAINER Yusukec Ltd

# Python起動の際の推奨
ENV PYTHONUNBUFFERED 1

# カレントフォルダのファイルをコピーする
COPY ./requirements.txt /requirements.txt

# dependenciesのインストール
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# セキュリティのため作成したユーザでの実行を推奨
# 通常だとroot権限のため、乗っ取られたときなんでもされてしまう。
RUN adduser -D user
USER user
