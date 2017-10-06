from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///nginx_log.sqlite")

db_session = scoped_session(sessionmaker(bind=engine))

Base_class = declarative_base()
Base_class.query = db_session.query_property()

class Log(Base_class):
    __tablename__ = "log"
    ID = Column(Integer, primary_key=True)
    IP = Column(String(20))
    METHOD = Column(String(5))
    CODE = Column(Integer)

    def __init__(self, ip=None, method=None, code=None):
        self.IP = ip
        self.METHOD = method
        self.CODE = code

if __name__ == "__main__":
    Base_class.metadata.create_all(bind=engine)
