from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from hackathon.models import Base
from hackathon.settings import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL)

Base.metadata.create_all(bind=engine, checkfirst=True)


def get_session():
    with Session(engine) as session:
        yield session
