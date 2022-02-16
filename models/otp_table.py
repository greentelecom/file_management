from sqlalchemy import Column, Integer, String, DateTime, text
import sys

sys.path.append("./utilities")
from database_connect import SessionBase, engine, Session


class OtpMessage(SessionBase):
    __tablename__ = 'tbl_otp_message'

    otp_id = Column('OTP_ID', Integer, primary_key=True)
    otp_message = Column('OTP_MESSAGE', String(60), nullable=False)
    msisdn = Column('MSISDN', String(60), index=True, unique=True)
    last_update = Column('LAST_UPDATE', String(60))
    record_date = Column('RECORD_DATE', DateTime, server_default=text('NOW()'))

    def __init__(self, otp_message, msisdn,last_update):
        self.otp_message = otp_message
        self.msisdn = msisdn
        self.last_update = last_update