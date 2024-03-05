FROM python:3.12-slim-bookworm
WORKDIR /code
ENV FLASK_APP=app
ENV FLASK_DEBUG=1
RUN adduser --uid 1000 --disabled-password --gecos '' invenio

COPY /app/requirements.txt ./
# COPY /app/requirements-depositor-modules.txt ./

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/code/app

ENV PYTHONPATH=$PYTHONPATH:/code/app/modules/depositor_admin_setting
ENV PYTHONPATH=$PYTHONPATH:/code/app/modules/depositor_item_register
ENV PYTHONPATH=$PYTHONPATH:/code/app/modules/depositor_login
ENV PYTHONPATH=$PYTHONPATH:/code/app/modules/depositor_models
ENV PYTHONPATH=$PYTHONPATH:/code/src/grobid_client

ENV INVENIO_WEB_HOST=127.0.0.1
ENV INVENIO_WEB_INSTANCE=invenio
ENV INVENIO_WEB_VENV=invenio
ENV INVENIO_WEB_HOST_NAME=invenio
ENV INVENIO_USER_EMAIL=wekosoftware@nii.ac.jp
ENV INVENIO_USER_PASS=uspass123
ENV INVENIO_POSTGRESQL_HOST=postgresql
ENV INVENIO_POSTGRESQL_DBNAME=invenio
ENV INVENIO_POSTGRESQL_DBUSER=invenio
ENV INVENIO_POSTGRESQL_DBPASS=dbpass123
ENV INVENIO_WORKER_HOST=127.0.0.1
ENV INVENIO_DB_POOL_CLASS=QueuePool

# 一時ファイルを置くフォルダのパス、コンテナ内のフォルダを参照しているため絶対パスで指定するとコンテナ内でのみ一時フォルダが生成される。
# マウントされている位置のパスを指定するとローカルにも保存される。
ENV TMPORARY_FILE_PATH=./tmp/

RUN apt-get update
RUN apt-get -y install libpq-dev
RUN apt-get install gcc -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
