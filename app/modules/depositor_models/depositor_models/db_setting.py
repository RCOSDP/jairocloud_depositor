import os

from typing import NoReturn

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, event, util, DateTime
from werkzeug.local import LocalProxy
from werkzeug.utils import import_string
from datetime import datetime
from sqlalchemy.dialects import mysql, postgresql

HOST_NAME=os.environ.get("INVENIO_POSTGRESQL_HOST") #postgresql
DBNAME=os.environ.get("INVENIO_POSTGRESQL_DBNAME") #invenio
DBPASS=os.environ.get("INVENIO_POSTGRESQL_DBPASS") #dbpass123
DBUSER=os.environ.get("INVENIO_POSTGRESQL_DBUSER") #invenio

# 接続先DBの設定
DATABASE = HOST_NAME+"://"+DBUSER+":"+DBPASS+"@"+HOST_NAME+":5432/"+ DBNAME 
# DATABASE = 'postgresql://invenio:dbpass123@postgresql:5432/invenio'

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

class Timestamp(object):
    """Timestamp model mix-in with fractional seconds support.

    SQLAlchemy-Utils timestamp model does not have support for
    fractional seconds.
    """

    created = db.Column(
        DateTime().with_variant(mysql.DATETIME(fsp=6), 'mysql'),
        default=datetime.utcnow,
        nullable=False
    )
    updated = db.Column(
        DateTime().with_variant(mysql.DATETIME(fsp=6), 'mysql'),
        default=datetime.utcnow,
        nullable=False
    )
    
Base = declarative_base()
Base.query = session.query_property()

def init_db(app):
    db.init_app(app)