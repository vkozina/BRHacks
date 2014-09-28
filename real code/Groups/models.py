from sqlalchemy import Column, Integer, String, Text
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(120))
    profile = Column(Text(400))

    def __init__(self, name=None, password=None, profile=None):
        self.name = name
        self.password = password
        self.profile = profile

    def __repr__(self):
        return '<User %r>' % (self.name)


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    text = Column(String(120))
    contact = Column(String(50))

    def __init__(self, title=None, text=None, contact=None):
        self.title = title
        self.text = text
        self.contact = contact

    def __repr__(self):
        return '<Groups %r>' % (self.title)