from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

## CREATES TEMP DB THAT WILL BE WIPED ON RESTART OF SERVER
engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
## SET UP A PRESET DB SESSION THAT YOU MUST COMMIT/FLUSH MANUALLY
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

## CREATE A BASE CLASS FOR ALL MODELS
Base = declarative_base()
Base.query = db_session.query_property()


## START DB
def init_db():
    ## IMPORT ALL OUR MODELS
    import models
    Base.metadata.create_all(bind=engine)
