from sqlalchemy import create_engine, Column, Integer, String, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///statistics_word_en/db.db', echo=True)
Base = declarative_base()


class Waste(Base):
    __tablename__ = 'tb_waste'
    id = Column(Integer, primary_key=True)
    word = Column(String)


class Word(Base):
    __tablename__ = 'tb_word'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    amount = Column(Integer, default=0)
    explain = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class WasteDao(object):
    @staticmethod
    def add(new_waste):
        exist = session.query(Waste).filter(Waste.word == new_waste.word).first()
        if not exist:
            session.add(new_waste)
            session.commit()

    @staticmethod
    def remove(word):
        session.delete(session.query(Waste).filter(Waste.word == word).first())
        session.commit()

    @staticmethod
    def query_wastes():
        return session.query(Waste).order_by(Waste.id).all()


class WordDao(object):

    @staticmethod
    def add(new_word):
        exist = session.query(Word).filter(Word.word == new_word.word).first()
        if exist:
            session.query(Word).filter(Word.word == new_word.word).update(
                {Word.amount: exist.amount + new_word.amount})
        else:
            session.add(new_word)
            session.commit()

    @staticmethod
    def update(word, explain):
        session.query(Word).filter(Word.word == word).update({Word.explain: explain})
        session.commit()

    @staticmethod
    def query_words():
        return session.query(Word.word, Word.amount).order_by(desc(Word.amount)).all()

    @staticmethod
    def query_by_word(word):
        return session.query(Word.explain).filter(Word.word == word).first()
