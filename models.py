from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(String, primary_key=True)
    status = Column(String, default='pending')
    worker_id = Column(String)
    priority = Column(Integer)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

engine = create_engine('sqlite:///tasks.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

