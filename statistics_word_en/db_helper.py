from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///statistics_word_en/db.db', echo=True)
Base = declarative_base()


class Waste(Base):
    __tablename__ = 'tb_waste'
    id = Column(Integer, primary_key=True)
    word = Column(String)


class Statistics(Base):
    __tablename__ = 'tb_statistics'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    amount = Column(Integer, default=0)


class Word(Base):
    __tablename__ = 'tb_word'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    explain = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class ExclusionDao(object):
    pass


class StatisticsDao(object):
    pass


class WordDao(object):
    pass