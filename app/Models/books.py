from app.extensions import db
from datetime import datetime




class Book(db.Model):
    __tablename__="books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    pages = db.Column(db.Integer,nullable=False)
    price_unit = db.Column(db.String(50),nullable=False ,default='UGX')
    publication_date = db.Column(db.Date,nullable=False) # the day the book was created
    isbn = db.Column(db.String(30),nullable=True, unique=True) # identifies published books
    genre = db.Column(db.String(50),nullable=False) # stores catergory of books
    description = db.Column(db.String(255),nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id')) # track the company id to which each book belongs
    company_id = db.Column(db.Integer,db.ForeignKey('companies.id'))
    author = db.relationship('Author',backref='books') # each book will belong to an author
    company = db.relationship('Company',backref='books')
    created_at =db.Column(db.DateTime,default= datetime.now())
    updated_at =db.Column(db.DateTime,onupdate= datetime.now())


# book constructor
    def __init__(self,title,pages,price_unit,company_id,author_id,publication_date,isbn,genre,description,):
        super(Book,self).__init__() # inherit from class db and ensures that neccessary class is executed
        self.title = title
        self.pages = pages
        self.price_unit = price_unit
        self.publication_date = publication_date
        self.isbn = isbn
        self.genre = genre
        self.description = description
        self.author_id = author_id
        self.company_id = company_id

    # string representation
    def __repr__(self):
       return f"Book{self.title}" 
    
