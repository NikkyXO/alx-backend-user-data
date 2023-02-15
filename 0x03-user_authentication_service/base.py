from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()

SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:410208olA$$$@localhost/a_db"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
