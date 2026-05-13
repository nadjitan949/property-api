from database.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(username={self.firstname} {self.lastname})>"