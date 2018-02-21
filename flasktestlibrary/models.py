from sqlalchemy import Column, Integer, String
from database import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    bookname = Column(String(50), unique=True)

    def __init__(self, bookname):
        self.bookname = bookname

    def __repr__(self):
        return 'book: %s' % self.bookname


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    authorname = Column(String(50), unique=True)

    def __init__(self, authorname):
        self.authorname = authorname

    def __repr__(self):
        return 'author: %s' % self.authorname

class AuthorBook(Base):
    __tablename__ = 'authorbook'
