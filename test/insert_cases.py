from tablecache.cache import CacheMixin
from redis.client import Redis
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


db_session = scoped_session(sessionmaker())
DeclarativeBase = declarative_base()

redis_session = Redis()


class TestTable(DeclarativeBase, CacheMixin):
    _redis_session = redis_session
    _app_id = 'test'
    _session = db_session

    __tablename__ = 'test_table'

    id = Column(Integer, primary_key=True)
    t1 = Column(String, nullable=False)

    @classmethod
    def add(cls, t1):
        record = cls(t1=t1)
        print (dir(db_session))
        db_session().add(record)
        db_session().commit()
        db_session().flush()
        return record


def test_case1():
    tb = TestTable()
    tb.add('2')
