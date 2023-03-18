from sqlalchemy import Column, Integer, String, Text, DateTime, BOOLEAN
from db.database import Base

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, nullable=False)
    product = Column(String, nullable=False)
    building_blocks = Column(String, nullable=False)
    iterations = Column(Integer, nullable=False)
    exp_topk = Column(Integer, nullable=False)
    route_topk = Column(Integer, nullable=False)
    beam_size = Column(Integer, nullable=False)
    retrieval = Column(BOOLEAN, nullable=False)
    retrieval_db = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=True)
    status = Column(Integer, nullable=False, default=2)
    result = Column(Text, nullable=True)