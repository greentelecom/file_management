from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:@localhost/bank_files?host=127.0.0.1?port=3306",pool_timeout=20, pool_recycle=299)
session_factory = sessionmaker(autocommit=False, autoflush=False,bind=engine)
Session = scoped_session(session_factory)
SessionBase = declarative_base()