from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fsdemo.config import Config

engine = create_engine(Config.DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


# Initialize database and tables follow the step below in command line mode.
# --------------------------------------------------------------------------
#   $ python3
#   >>> from fsdemo.db import init_db
#   >>> init_db()
# --------------------------------------------------------------------------
def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # eg. import yourapplication.models
    import fsdemo.models
    fsdemo.models
    Base.metadata.create_all(bind=engine)
