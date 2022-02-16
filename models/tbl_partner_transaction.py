from sqlalchemy import Column, Integer, String, DateTime, text, Text, BLOB
import sys

sys.path.append("../utilities_core")
from database_connect import SessionBase


class PartnerTxn(SessionBase):
    __tablename__ = 'partner_transactions'

    txn_id = Column('TXN_ID', Integer, primary_key=True)
    institution = Column('INSTITUTION', String(200), nullable=False)
    transaction_ref = Column('transaction_ref', String(35), nullable=False, index=True)
    account = Column('account', String(25), index=True, nullable=False)
    amount = Column('amount', String(10), server_default='0', nullable=False)
    transaction_time = Column('transaction_time', DateTime, server_default=text('NOW()'))