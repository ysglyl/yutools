from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.db', echo=True)
Base = declarative_base()

'''
id content begin_date deadline frequency repeat auto_expire complete_rate 
degree_importance degree_urgency status

'''
class Plan(Base):
    __tablename__ = 'tb_plan'
    id = Column(Integer,primary_key=True)
    content = Column(String)
