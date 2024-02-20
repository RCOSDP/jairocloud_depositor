
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

# 接続先DBの設定
DATABASE = 'postgresql://invenio:dbpass123@192.168.56.111:25401/invenio??charset=utf8'

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