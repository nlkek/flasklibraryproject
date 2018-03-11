from init import dbs

ROLE_USER = 0
ROLE_ADMIN = 1

books_authors = dbs.Table('books_authors',
                          dbs.Column('book_id', dbs.Integer, dbs.ForeignKey('book.id'), primary_key=True),
                          dbs.Column('author_id', dbs.Integer, dbs.ForeignKey('author.id'), primary_key=True)
                          )


class Book(dbs.Model):
    __tablename__ = 'books'
    id = dbs.Column(dbs.Integer, primary_key=True)
    bookname = dbs.Column(dbs.String(50), unique=True)

    def __repr__(self):
        return 'book: %s' % self.bookname


class Author(dbs.Model):
    __tablename__ = 'authors'
    id = dbs.Column(dbs.Integer, primary_key=True)
    authorname = dbs.Column(dbs.String(50), unique=True)

    def __repr__(self):
        return 'author: %s' % self.authorname


class User(dbs.Model):
    id = dbs.Column(dbs.Integer, primary_key=True)
    login = dbs.Column(dbs.String(50), unique=True)
    password = dbs.Column(dbs.String(50))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id



