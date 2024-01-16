from datetime import datetime

from flask_security import RoleMixin, UserMixin
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy import Column, Integer, String, Float, DateTime,  and_, asc, desc, func, or_
from db_setting import Engine, Base, db

from models import User as _User
from models import Affiliation_Id as _Affiliation_Id
from models import Affiliation_Repository as _Affiliation_Repository

class Affiliation_Repository(object):
    """operated on the Affiliation repository"""
    def create_aff_repository(self, aff_repository):
        """
        create new aff_repository
        :param aff_repository:
        :return:
        """
        assert aff_repository
        try:
            with db.session.begin_nested():
                db.session.execute(_Affiliation_Repository.__table__.insert(), aff_repository)
            db.session.commit()
            return aff_repository
        except Exception as ex:
            db.session.rollback()
            return None
        
    def upt_aff_repository(self, aff_repository):
        assert aff_repository
        try:
            with db.session.begin_nested():
                _aff_repository = _User.query.filter_by(id=aff_repository.get('id')).one_or_none()
                if _aff_repository:
                    _aff_repository.affiliation_id = aff_repository.get('affiliation_id')
                    _aff_repository.role = aff_repository.get('repository_url')
                    _aff_repository.access_token = aff_repository.get('access_token')
                    db.session.merge(_aff_repository)
            db.session.commit()
            return _aff_repository
        except Exception as ex:
            db.session.rollback()
            return None

    def get_aff_repository_by_affiliation_id(self, affiliation_id):
        with db.session.autoflush():
            query = _Affiliation_Repository.query.filter(affiliation_id=affiliation_id)
            return query.one_or_none()


class User(object):
    """operated on the user"""
    def create_user(self, user):
        """ create new user
        :param user:
        :return:
        """
        assert user
        try:
            with db.session.begin_nested():
                db.session.execute(_User.__table__.insert(), user)
            db.session.commit()
            return user
        except Exception as ex:
            db.session.rollback()
            return None
        
    def upt_user(self, user):
        assert user
        try:
            with db.session.begin_nested():
                _user = _User.query.filter_by(id=user.get('id')).one_or_none()
                if _user:
                    _user.affiliation_id = user.get('affiliation_id')
                    _user.user_orcid = user.get('user_orcid')
                    _user.role = user.get('role')
                    db.session.merge(_user)
            db.session.commit()
            return _user
        except Exception as ex:
            db.session.rollback()
            return None

    def get_user_by_user_id_and_affiliation_id(self, user_id, affiliation_id):
        with db.session.no_autoflush:
            query = _User.query.filter(and_(_User.user_id == user_id,
                                            _User.affiliation_id == affiliation_id))
            return query.one_or_none()

    def get_users_by_user_id(self, user_id):
        with db.session.no_autoflush:
            query = _User.query.filter(user_id=user_id)
            return query.all()

    def get_users_by_affiliation_id(self, affiliation_id):
        with db.session.no_autoflush:
            query = _User.query.filter(affiliation_id=affiliation_id)
            return query.all()
        
    
class Affiliation_Id(object):
    """
    operated on the Affiliation ID
    """
    def create_affiliation_id(self, affiliation_idp_url, affiliation_name):
        """
        create new affiliation_id
        :param affiliation_id: class _Affiliation_Id
        :return:
        """
        assert affiliation_idp_url
        assert affiliation_name
        affiliation_id = _Affiliation_Id(affiliation_idp_url=affiliation_idp_url, affiliation_name=affiliation_name)
        try:
            with db.session.begin_nested():
                db.session.execute(_Affiliation_Id.__table__.insert(), affiliation_id)
            db.session.commit()
            return affiliation_id
        except Exception as ex:
            db.session.rollback()
            return None

    def upt_affiliation_id(self, affiliation_id):
        assert affiliation_id
        try:
            with db.session.begin_nested():
                _affliation_id = _Affiliation_Id.query.filter_by(id=affiliation_id.get('id')).one_or_none()
                if _affliation_id:
                    _affliation_id.affiliation_idp_url = affiliation_id.get('affiliation_idp_url')
                    _affliation_id.affiliation_name = affiliation_id.get('affiliation_name')
                    db.session.merge(_affliation_id)
            db.session.commit()
            return _affliation_id
        except Exception as ex:
            db.session.rollback()
            return None
        
    def get_affiliation_id_by_id(self, affiliation_id):
        with db.session.no_autoflush():
            query = _Affiliation_Id.query.filter_by(id = affiliation_id)
            return query.one_or_none()
        
    def get_affiliation_id_by_idp_url(self, idp_url):
        with db.session.no_autoflush():
            query = _Affiliation_Id.query.filter_by(affiliation_idp_url = idp_url)
            return query.one_or_none()
    
