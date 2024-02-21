from datetime import datetime
from flask import current_app
from flask_security import RoleMixin, UserMixin
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy import Column, Integer, String, Float, DateTime,  and_, asc, desc, func, or_
from db_setting import Engine, Base, db

from modules.models import User as _User
from modules.models import Affiliation_Id as _Affiliation_Id
from modules.models import Affiliation_Repository as _Affiliation_Repository

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
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(ex)
            raise
        
        return aff_repository
        
    def upt_aff_repository(self, aff_repository):
        assert aff_repository
        try:
            with db.session.begin_nested():
                _aff_repository = _Affiliation_Repository.query.filter_by(id=aff_repository.get('id')).one_or_none()
                if _aff_repository:
                    _aff_repository.affiliation_id = aff_repository.get('affiliation_id')
                    _aff_repository.repository_url = aff_repository.get('repository_url')
                    _aff_repository.access_token = aff_repository.get('access_token')
                    db.session.merge(_aff_repository)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(ex)
            raise
        
        return _aff_repository

    def get_aff_repository_by_affiliation_id(self, affiliation_id):
        with db.session.no_autoflush:
            query = _Affiliation_Repository.query.filter_by(affiliation_id=affiliation_id)
            return query.one_or_none()
        
    def get_affiliation_repository_list(self):
        """Get affiliation_repository list info.

        :return:
        """
        with db.session.no_autoflush:
            query = _Affiliation_Repository.query.filter_by().order_by(asc(_Affiliation_Repository.id))
            return query.all()


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
                db.session.add(user)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(ex)
            raise
        
        return user
        
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
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(ex)
            raise
        
        return _user
        
    def get_user_by_id(self, id):
        with db.session.no_autoflush:
            query = _User.query.filter_by(id=id)
            return query.one_or_none()

    def get_user_by_user_id(self, user_id):
        with db.session.no_autoflush:
            query = _User.query.filter_by(user_id=user_id)
            return query.one_or_none()

    def get_users_by_affiliation_id(self, affiliation_id):
        with db.session.no_autoflush:
            query = _User.query.filter_by(affiliation_id=affiliation_id)
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
                db.session.add(affiliation_id)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(ex)
            raise
        
        return affiliation_id

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
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(ex)
            raise
        
        return _affliation_id
        
    def get_affiliation_id_by_id(self, affiliation_id):
        # with db.session.no_autoflush():
        query = _Affiliation_Id.query.filter_by(id = affiliation_id)
        return query.one_or_none()
        
    def get_affiliation_id_by_idp_url(self, affiliation_idp_url):
        # with db.session.no_autoflush():
        query = _Affiliation_Id.query.filter_by(affiliation_idp_url = affiliation_idp_url)
        return query.one_or_none()
    
    def get_affiliation_id_by_affiliation_name(self, affiliation_name):
        # with db.session.no_autoflush():
        query = _Affiliation_Id.query.filter_by(affiliation_name = affiliation_name)
        return query.one_or_none()
    
    def get_affiliation_id_list(self):
        """Get affiliation_name list info.

        :return:
        """
        with db.session.no_autoflush:
            query = _Affiliation_Id.query.filter_by().order_by(asc(_Affiliation_Id.id))
            return query.all()

