FROM python:3.7-alpine
MAINTAINER Yusukec Ltd

# Python起動の際の推奨
ENV PYTHONUNBUFFERED 1

# カレントフォルダのファイルをコピーする
COPY ./requirements.txt /requirements.txt

# POSTGRESのdependenciesのインストール
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

# dependenciesのインストール
RUN pip install -r /requirements.txt

# POSTGRESQL系
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# シェアファイルのフォルダ設定
# メディアファイルの置き場所
RUN mkdir -p /vol/web/media
# javascriptやcssなど、静的ファイルの置き場所
RUN mkdir -p /vol/web/static
# -pは途中のフォルダがなければ作る。ここではvol, webなど。

# セキュリティのため新規作成したユーザでの実行を推奨
# 通常だとroot権限のため、乗っ取られたときなんでもされてしまう。
RUN adduser -D user

# シェアフォルダの権限設定を作成したユーザに変える。
RUN chown -R user:user /vol/
# ユーザだけがW/R可能。他の人はRのみ。
RUN chmod -R 755 /vol/web

USER user
