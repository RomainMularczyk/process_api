from sqlalchemy import Column, Integer, Float, String, DateTime
from database.config import Base

class Process(Base):
    __tablename__ = "process_usage"
    id = Column(Integer, primary_key=True)
    process = Column(String, index=True)
    user = Column(String, index=True)
    cpu = Column(Float)
    memory = Column(Float)
    command = Column(String)
    time = Column(DateTime)
