from sqlmodel import SQLModel, create_engine, Session
from .models.cookies_model import Cookies
from api.config import DATABASE_URL


class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        session = Session(self.engine)
        return session

    def update_cookies(self, cookies: Cookies):
        self.create_tables()
        with self.get_session() as session:
            session.merge(cookies)
            session.commit()
