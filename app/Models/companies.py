from app.extensions import db
from datetime import datetime

class Company(db.Model):
     __tablename__= 'companies'
     id = db.Column(db.Integer,primary_key =True)    # primary key uniquely identify the user
     name = db.Column(db.String(100),unique =True)
     origin = db.Column(db.String(100),nullable=False)
     description = db.Column(db.Text(),nullable=False)
     author_id= db.Column(db.Integer, db.ForeignKey('authors.id'))
     author = db.relationship('Author',backref='companies')
     created_at =db.Column(db.DateTime,default= datetime.now())
     updated_at =db.Column(db.DateTime,onupdate= datetime.now())

    

# id's are automatically incremeneted
# creating the constructor for the  new instance company
     def __init__(self,name,origin,description,author_id):
      super(Company,self).__init__()
      self.name = name
      self.origin = origin
      self.description = description
      self.author_id = author_id


     #  every new company will be an object
     # adding a string representattions for the companies to be created
     # repr represents 
     def __repr__(self):
        return f"{self.name}{self.origin}"




