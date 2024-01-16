from datetime import datetime

from flask_security import RoleMixin, UserMixin
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy import Column, Integer, String, Float, DateTime, Sequence
from db_setting import Engine, Base, db

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

class User(db.Model, UserMixin, Timestamp):
    """User data model."""

    __tablename__ = "user"

    id = db.Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True, default=Sequence("user_id_seq"))

    user_id = db.Column(String(80), nullable=False)

    affiliation_id = db.Column(Integer, nullable=False)

    user_orcid = db.Column(String(80))

    role = db.Column(String(80))

class Affiliation_Repository(db.Model, Timestamp):
    """Affiliationrepository data model"""

    __tablename__ = "affiliation_repository"

    id = db.Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True, default=Sequence("affiliation_repository_id_seq"))

    affiliation_id = db.Column(Integer, nullable=False)

    repository_url = db.Column(String(80), nullable=False)

    access_token = db.Column(String(80), nullable=False)

class Affiliation_Id(db.Model, Timestamp):
    """Affiliation ID data model"""

    __tablename__ = "affiliation_id"

    id = db.Column(Integer,  primary_key=True, nullable = False, unique=True, autoincrement=True, default=Sequence("affiliation_id_id_seq"))

    affiliation_idp_url = db.Column(String(80), nullable=False)

    affiliation_name = db.Column(String(80), nullable=False)