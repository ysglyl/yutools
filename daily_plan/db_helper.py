import enum
import datetime
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
    status_label = {0: 'Wait', 1: 'Going', 2: 'Done', 3: 'Cancel', 4: 'Expire'}

    @staticmethod
    def add_actions(actions, plan_id):
        for action in actions:
            action.plan_id = plan_id
            if action.begin_date == datetime.date.today():
                action.status = 1
            else:
                action.status = 0
        session.add_all(actions)
        session.commit()

    @staticmethod
    def update_action(act_id, status):
        session.query(Action).filter(Action.id == act_id).update(
            {Action.status: status, Action.complete_time: datetime.date.today()})
        session.commit()

    @staticmethod
    def auto_update_action():
        session.query(Action).filter(and_(Action.status == 0, Action.begin_date <= datetime.date.today())).update(
            {Action.status: 1})
        session.commit()
        session.query(Action).filter(and_(Action.status == 0, Action.deadline < datetime.date.today())).update(
            {Action.status: 4})
        session.commit

    @staticmethod
    def query_actions(tb_index, filter_status):
        query = session.query(Action)
        if tb_index == 1:
            query = query.filter(
                and_(Action.degree_importance == True, Action.degree_urgency == True))
        elif tb_index == 2:
            query = query.filter(
                and_(Action.degree_importance == True, Action.degree_urgency == False))
        elif tb_index == 3:
            query = session.query(Action).filter(
                and_(Action.degree_importance == False, Action.degree_urgency == False))
        elif tb_index == 4:
            query = session.query(Action).filter(
                and_(Action.degree_importance == False, Action.degree_urgency == True))
        if filter_status in [0, 1, 2, 3, 4]:
            query = query.filter(Action.status == filter_status)
        elif filter_status == 5:
            query = query.filter(Action.status.in_([0, 1]))
        elif filter_status == 6:
            pass
        else:
            query = query.filter(Action.status == -1)
        return query.order_by(Action.begin_date).all()
