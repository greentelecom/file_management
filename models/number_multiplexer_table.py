from sqlalchemy import Column, Integer, String, DateTime, text, func
import sys

sys.path.append("./utilities")
from database_connect import SessionBase, engine, Session


class NumberMultiplexer(SessionBase):
    __tablename__ = "tbl_number_multiplexer"
    mt_id = Column('MT_ID', Integer, primary_key=True)
    mno = Column('MNO', String(40), nullable=False)
    mobile_money_channel = Column('MOBILE_MONEY_CHANNEL', String(20), nullable=False)
    msisdn_prefix = Column('MSISDN_PREFIX', String(20), nullable=False, index=True)
    record_date = Column('RECORD_DATE', DateTime, nullable=False, server_default=func.now())
