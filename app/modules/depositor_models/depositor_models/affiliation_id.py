from flask import current_app
from sqlalchemy import Column, Integer, String, Float, DateTime, Sequence, asc
from .db_setting import db, Timestamp

class Affiliation_Id(db.Model, Timestamp):
    """Affiliation ID data model"""

    __tablename__ = "affiliation_id"
    
    __table_args__={'extend_existing': True}

    id = db.Column(Integer,  primary_key=True, nullable = False, unique=True, autoincrement=True, default=Sequence("affiliation_id_id_seq"))

    affiliation_idp_url = db.Column(String(80), nullable=False)

    affiliation_name = db.Column(String(80), nullable=False)
    

class Affiliation_Id_manager(object):
    """
    operated on the Affiliation ID
    """
    @classmethod
    def create_affiliation_id(cls, affiliation_id):
        """
        create new affiliation_id
        :param affiliation_id: class Affiliation_Id
        :return:
        """
        assert affiliation_id
        try:
            with db.session.begin_nested():
                db.session.add(affiliation_id)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(ex)
            raise ex
        
        return affiliation_id

    @classmethod
    def get_affiliation_id_by_id(cls, affiliation_id):
        # with db.session.no_autoflush():
        query = Affiliation_Id.query.filter_by(id = affiliation_id)
        return query.one_or_none()

    @classmethod  
    def get_affiliation_id_by_idp_url(cls, affiliation_idp_url):
        # with db.session.no_autoflush():
        query = Affiliation_Id.query.filter_by(affiliation_idp_url = affiliation_idp_url)
        return query.one_or_none()

    @classmethod
    def get_affiliation_id_by_affiliation_name(cls, affiliation_name):
        # with db.session.no_autoflush():
        query = Affiliation_Id.query.filter_by(affiliation_name = affiliation_name)
        return query.one_or_none()
    
    @classmethod
    def get_affiliation_id_list(cls):
        """Get affiliation_name list info.

        :return:
        """
        with db.session.no_autoflush:
            query = Affiliation_Id.query.filter_by().order_by(asc(Affiliation_Id.id))
            return query.all()

