from sqlalchemy import Column, Integer, String, Text, DateTime
from fsdemo.db import Base
from datetime import datetime


class BTags(Base):
    __tablename__ = 'btags'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    addtime = Column(DateTime, nullable=False, default=datetime.now)
    updatetime = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, name=None):
        self.name = name


class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    tags = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    addtime = Column(DateTime, nullable=False, default=datetime.now)
    updatetime = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, title=None, tags=None, content=None):
        self.title = title
        self.tags = tags
        self.content = content


class GTags(Base):
    __tablename__ = 'gtags'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    addtime = Column(DateTime, nullable=False, default=datetime.now)
    updatetime = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, name=None):
        self.name = name


class Gallery(Base):
    __tablename__ = 'gallery'
    id = Column(Integer, primary_key=True)
    link = Column(String(255), nullable=False)
    tags = Column(Text, nullable=False)
    caption = Column(Text, nullable=False)
    addtime = Column(DateTime, nullable=False, default=datetime.now)
    updatetime = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, link=None, tags=None, caption=None):
        self.link = link
        self.tags = tags
        self.caption = caption
