
from typing import NoReturn

from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, event, util

# 接続先DBの設定
DATABASE = 'postgresql:///invenio:dbpass123@localhost:25401/invenio'

Engine = create_engine(
  DATABASE,
  encoding="utf-8",
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
class SQLAlchemy(FlaskSQLAlchemy):
    """Implement or overide extension methods."""

    def apply_driver_hacks(self, app, info, options):
        """Call before engine creation."""
        # Don't forget to apply hacks defined on parent object.
        super(SQLAlchemy, self).apply_driver_hacks(app, info, options)

        # Set database pool connection
        self.__set_db_connection_pool(app, options)

    @staticmethod
    def __set_db_connection_pool(app: object, options: dict) -> NoReturn:
        """Set database connection pool.

        :param app: Invenio app.
        :param options: The `options` parameter is
        a dictionary of keyword arguments that will then be used to call
        the :func:`sqlalchemy.create_engine` function.
        """
        try:
            str_pool_class = app.config['DB_SQLALCHEMY_POOL_PACKAGE'] + '.' + \
                app.config['DB_POOL_CLASS']
            pool_class = import_string(
                str_pool_class)
        except Exception as error:
            pool_class = QueuePool
            app.logger.debug(error)
        options.setdefault('poolclass', pool_class)
        options.setdefault('pool_pre_ping', True)


def do_sqlite_connect(dbapi_connection, connection_record):
    """Ensure SQLite checks foreign key constraints.

    For further details see "Foreign key support" sections on
    https://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#foreign-key-support
    """
    # Enable foreign key constraint checking
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


def do_sqlite_begin(dbapi_connection):
    """Ensure SQLite transaction are started properly.

    For further details see "Foreign key support" sections on
    https://docs.sqlalchemy.org/en/rel_1_0/dialects/sqlite.html#pysqlite-serializable # noqa
    """
    # emit our own BEGIN
    dbapi_connection.execute('BEGIN')
    
db = SQLAlchemy(metadata=metadata)


Base = declarative_base()
Base.query = session.query_property()

