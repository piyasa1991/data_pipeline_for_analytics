from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime



Base = declarative_base()

class Logs(Base):
    """
    ORM Model for the table installs_by_country
    
    Arguments:
        Base {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    __tablename__ = 'logs'
    index = Column(Integer, primary_key=True)
    raw_log = Column(String,nullable=False,unique=True)
    remote_addr = Column(String)
    time_local = Column(String)
    request_type = Column(String)
    request_path = Column(String)
    status=Column(Integer)
    body_bytes_sent=Column(Integer)
    http_referer = Column(String)
    http_user_agent = Column(String)
    created=Column(TIMESTAMP,default=datetime.now())

    # def __repr__(self):
    #     return "InstallByCountry(index='{}', country='{}', created_at={}, paid={}, installs={})" \
    #         .format(self.index, self.country, self.created_at, self.paid, self.installs)