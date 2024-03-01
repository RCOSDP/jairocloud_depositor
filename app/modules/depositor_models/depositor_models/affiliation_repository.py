from flask import current_app
from sqlalchemy import Column, Integer, String, and_, asc, desc, func, or_, Sequence
from .db_setting import db, Timestamp

class Affiliation_Repository(db.Model, Timestamp):
    """Affiliationrepository data model"""

    __tablename__ = "affiliation_repository"
    
    __table_args__={'extend_existing': True}

    id = db.Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True, default=Sequence("affiliation_repository_id_seq"))

    affiliation_id = db.Column(Integer, nullable=False)

    repository_url = db.Column(String(80), nullable=False)

    access_token = db.Column(String(80), nullable=False)
    
    
class Affiliation_Repository_manager(object):
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
                db.session.execute(Affiliation_Repository.__table__.insert(), aff_repository)
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
                _aff_repository = Affiliation_Repository.query.filter_by(id=aff_repository.get('id')).one_or_none()
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
            query = Affiliation_Repository.query.filter_by(affiliation_id=affiliation_id)
            return query.one_or_none()
        
    def get_aff_repository_by_affiliation_name(self, affiliation_name):
        with db.session.no_autoflush:
            affiliation_id = Affiliation_Id().get_affiliation_id_by_affiliation_name(affiliation_name)
            if affiliation_id:
                aff_repository = self.get_aff_repository_by_affiliation_id(affiliation_id.id)
            else :
                return None
            return aff_repository

    def get_affiliation_repository_list(self):
        """Get affiliation_repository list info.

        :return:
        """
        with db.session.no_autoflush:
            query = Affiliation_Repository.query.filter_by().order_by(asc(Affiliation_Repository.id))
            return query.all()

