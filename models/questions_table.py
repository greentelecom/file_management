from sqlalchemy import Integer, Column, String, DateTime, text, func
import sys
sys.path.append("./utilities_core")
from database_connect import SessionBase, Session


class Questions(SessionBase):
    __tablename__ = "tbl_qn_questions"

    id = Column('ID', Integer, primary_key=True)
    answer = Column('ANSWER', String(20))
    qn_weightage = Column('QN_WEIGHTAGE', Integer)
    question = Column('QUESTION', String(2000))
    category = Column('CATEGORY', String(50))
    record_date = Column('RECORD_DATE', DateTime, server_default=text('NOW()'))

    def __init__(self):
        self.answer = None;
        self.qn_weightage = None;
        self.question = None
        self.record_date = None;
        self.category = None

    @staticmethod
    def max_qn_count():
        max_id = Session().query(func.max(Questions.id).label('maxId')).scalar()
        return max_id;
