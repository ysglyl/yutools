import enum
from sqlalchemy import create_engine, \
    Column, Integer, String, Date, DateTime, Enum, Boolean, \
    and_, ForeignKey
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
    degree_importance = Column(Boolean)
    degree_urgency = Column(Boolean)


class Action(Base):
    __tablename__ = 'tb_action'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    begin_date = Column(Date)
    deadline = Column(Date)
    degree_importance = Column(Integer)
    degree_urgency = Column(Integer)
    status = Column(Integer)
    complete_time = Column(DateTime, nullable=True)
    plan_id = Column(Integer, ForeignKey('tb_plan.id'))


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


class ActionDao(object):
    @staticmethod
    def add_actions(actions):
        import datetime
        for action in actions:
            action.status = 0
            action.complete_time=datetime.datetime.now()
        session.add_all(actions)
        session.commit()

    @staticmethod
    def query_actions(filter_type):
        if filter_type == 1:
            return session.query(Action).filter(
                and_(Action.degree_importance == True, Action.degree_urgency == True)).order_by(Action.begin_date).all()
        elif filter_type == 2:
            return session.query(Action).filter(
                and_(Action.degree_importance == True, Action.degree_urgency == False)).order_by(
                Action.begin_date).all()
        elif filter_type == 3:
            return session.query(Action).filter(
                and_(Action.degree_importance == False, Action.degree_urgency == False)).order_by(
                Action.begin_date).all()
        elif filter_type == 4:
            return session.query(Action).filter(
                and_(Action.degree_importance == False, Action.degree_urgency == True)).order_by(
                Action.begin_date).all()
        else:
            return None
