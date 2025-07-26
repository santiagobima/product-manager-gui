from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///database/sqlalchemyproductos.db', echo=True)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

