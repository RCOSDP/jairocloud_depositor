FROM python:3.12-slim-bookworm
WORKDIR /code
ENV FLASK_APP=app
ENV FLASK_DEBUG=1
RUN adduser --uid 1000 --disabled-password --gecos '' depositor

COPY /app/requirements.txt ./
# COPY /app/requirements-depositor-modules.txt ./

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/code/app

ENV PYTHONPATH=$PYTHONPATH:/code/app/modules/depositor_admin_setting
ENV PYTHONPATH=$PYTHONPATH:/code/app/modules/depositor_item_register
ENV PYTHONPATH=$PYTHONPATH:/code/app/modules/depositor_login
ENV PYTHONPATH=$PYTHONPATH:/code/app/modules/depositor_models
ENV PYTHONPATH=$PYTHONPATH:/code/src/grobid_client

ENV DEPOSITOR_WEB_HOST=127.0.0.1
ENV DEPOSITOR_POSTGRESQL_HOST=postgresql
ENV DEPOSITOR_POSTGRESQL_DBNAME=depositor
ENV DEPOSITOR_POSTGRESQL_DBUSER=depositor
ENV DEPOSITOR_POSTGRESQL_DBPASS=dbpass123

# shibbolethログインがモックの為、パスワードは固定値
ENV MOCK_PASSWORD=testpass
# 一時ファイルを置くフォルダのパス、コンテナ内のフォルダを参照しているため絶対パスで指定するとコンテナ内でのみ一時フォルダが生成される。
# マウントされている位置のパスを指定するとローカルにも保存される。
ENV TMPORARY_FILE_PATH=./tmp/

RUN apt-get update
RUN apt-get -y install libpq-dev
RUN apt-get install gcc -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
