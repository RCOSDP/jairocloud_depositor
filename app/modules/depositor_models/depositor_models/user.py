from flask import current_app
from flask_security import RoleMixin, UserMixin
from sqlalchemy import Column, Integer, String, Float, DateTime, Sequence
from .db_setting import Engine, Base, db, Timestamp



class User(db.Model, UserMixin, Timestamp):
    """User data model."""

    __tablename__ = "user"
    
    __table_args__={'extend_existing': True}

    id = db.Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True, default=Sequence("user_id_seq"))

    is_active = True 

    user_id = db.Column(String(80), nullable=False)

    affiliation_id = db.Column(Integer, nullable=False)

    user_orcid = db.Column(String(80))

    role = db.Column(String(80))


class User_manager(object):
    """operated on the user"""
    @classmethod
    def create_user(cls, user):
        """ create new user
        :param user:
        :return:
        """
        assert user
        try:
            with db.session.begin_nested():
                db.session.add(user)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(ex)
            raise
        
        return user
    
    @classmethod
    def upt_user(cls, user):
        assert user
        try:
            with db.session.begin_nested():
                _user = User.query.filter_by(id=user.get('id')).one_or_none()
                if _user:
                    _user.affiliation_id = user.get('affiliation_id')
                    _user.user_orcid = user.get('user_orcid')
                    _user.role = user.get('role')
                    db.session.merge(_user)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(ex)
            raise
        
        return _user
    
    @classmethod
    def get_user_by_id(cls, id):
        with db.session.no_autoflush:
            query = User.query.filter_by(id=id)
            return query.one_or_none()

    @classmethod
    def get_user_by_user_id(cls, user_id):
        with db.session.no_autoflush:
            query = User.query.filter_by(user_id=user_id)
            return query.one_or_none()

    @classmethod
    def get_users_by_affiliation_id(cls, affiliation_id):
        with db.session.no_autoflush:
            query = User.query.filter_by(affiliation_id=affiliation_id)
            return query.all()
        
    