from postgres import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, TIMESTAMP, String
from datetime import datetime


class OldData(Base):
    __tablename__ = "dataset1"

    id = Column(Integer, primary_key=True)
    digits = Column(Integer, nullable=True)
    created_on = Column(TIMESTAMP, nullable=False, default=datetime.now())


class NewData(Base):
    __tablename__ = "dataset2"

    id = Column(Integer, primary_key=True)
    digits = Column(Integer, nullable=True)
    created_on = Column(TIMESTAMP, nullable=False, default=datetime.now())


class Result(Base):
    __tablename__ = "result"

    id = Column(Integer, autoincrement=False, primary_key=True)
    Value1 = Column(String, nullable=True)
    Value2 = Column(String, nullable=True)
