import enum
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///daily_plan/db.db', echo=True)
Base = declarative_base()


class PlanFrequency(enum.Enum):
    NoRepeat = 0
    Day = 1
    Week = 2
    Month = 3
    Quarter = 4
    Year = 5


class Plan(Base):
    __tablename__ = 'tb_plan'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    begin_date = Column(Date)
    deadline = Column(Date)
    frequency = Column(Enum(PlanFrequency))
    repeat = Column(Integer)
    degree_importance = Column(Integer)
    degree_urgency = Column(Integer)
    can_op_all = Column(Boolean)


class Action(Base):
    __tablename__ = 'tb_action'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    begin_date = Column(Date)
    deadline = Column(Date)
    degree_importance = Column(Integer)
    degree_urgency = Column(Integer)
    status = Column(Integer)
    complete_time = Column(DateTime)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class PlanDao(object):

    @staticmethod
    def add_plan(new_plan):
        session.add(new_plan)
        session.commit()
        return new_plan.id

    @staticmethod
    def query_plans():
        return session.query(Plan).order_by(Plan.id).all()

