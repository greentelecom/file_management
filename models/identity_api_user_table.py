import sys

# from sqlalchemy import Column, NUMBER, String, DATE, text, func
from passlib.apps import custom_app_context as pwd_context

from sqlalchemy.orm import Session

sys.path.append("./utilities_core")
from sqlalchemy import Column, Integer, String, DateTime, text,Numeric,func
from sqlalchemy.dialects.oracle import DATE,NUMBER
import datetime
# import sys

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from database_connect import SessionBase, engine, Session

class User(SessionBase):

    __tablename__ = 'tbl_identity_api_user'
    user_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    username = Column(String(100), nullable=False, index=True)  # server_default='NEW'
    password_hash = Column(String(128), nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user