import os

from typing import NoReturn

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, event, util
from werkzeug.local import LocalProxy
from werkzeug.utils import import_string

HOST_NAME=os.environ.get("INVENIO_POSTGRESQL_HOST") #postgresql
DBNAME=os.environ.get("INVENIO_POSTGRESQL_DBNAME") #invenio
DBPASS=os.environ.get("INVENIO_POSTGRESQL_DBPASS") #dbpass123
DBUSER=os.environ.get("INVENIO_POSTGRESQL_DBUSER") #invenio

# 接続先DBの設定
<<<<<<< Updated upstream
DATABASE = HOST_NAME+"://"+DBUSER+":"+DBPASS+"@"+HOST_NAME+":5432/"+ DBNAME 
# DATABASE = 'postgresql://invenio:dbpass123@192.168.56.111:25401/invenio??charset=utf8'
=======
DATABASE = 'postgresql://invenio:dbpass123@192.168.56.103:25401/invenio'
>>>>>>> Stashed changes

Engine = create_engine(
  DATABASE,
  echo=False
)

session = scoped_session(sessionmaker(bind = Engine))
NAMING_CONVENTION = util.immutabledict({
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
})
"""Configuration for constraint naming conventions."""

metadata = MetaData(naming_convention=NAMING_CONVENTION)
"""Default database metadata object holding associated schema constructs."""

db = SQLAlchemy(metadata=metadata)


Base = declarative_base()
Base.query = session.query_property()

def init_db(app):
    db.init_app(app)