from sqlalchemy import Column, Integer, String, DateTime, text, Text, BLOB
import sys

sys.path.append("./utilities_core")
from database_connect import SessionBase


class Admin(SessionBase):
    __tablename__ = 'tbl_identity_admin'

    sub_id = Column('SUB_ID', Integer, primary_key=True)
    device_id = Column('DEVICE_ID', String(100), nullable=False)
    msisdn = Column('MSISDN', String(60), index=True)
    mno = Column('MNO', String(15), index=True)
    finger_template = Column('FINGER_TEMPLATE', String(6000), nullable=True, index=True)
    passcode = Column('PASSCODE', String(15), nullable=False, index=True)
    activity_status = Column('ACTIVITY_STATUS', String(60), nullable=False, server_default='ACTIVE')
    last_update = Column('LAST_UPDATE', String(100))
    record_date = Column('RECORD_DATE', DateTime, server_default=text('NOW()'))
