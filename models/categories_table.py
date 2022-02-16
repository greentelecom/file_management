from sqlalchemy import Column, Integer, String, DateTime, text
import sys

sys.path.append("./utilities")
from database_connect import SessionBase, engine, Session


class QuestionCategoriese(SessionBase):
    __tablename__ = 'tbl_question_categories'

    otp_id = Column('CATEGORY_ID', Integer, primary_key=True)
    category_name = Column('CATEGORY_NAME', String(60), nullable=False)
    category_image = Column('CATEGORY_IMAGE', String(200), index=True, unique=True)
    record_date = Column('RECORD_DATE', DateTime, server_default=text('NOW()'))

    def __init__(self, category_name, category_image):
        self.category_name = category_name;
        self.category_image = category_image;