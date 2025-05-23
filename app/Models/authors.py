# import the db object
from  app.extensions import db
from datetime import datetime

# creating the table to store the columns
class Author(db.Model):   # db the datatype of that column
     __tablename__ = "authors"  # it shuold be differ from the table name
     id = db.Column(db.Integer,primary_key =True)    # primary key uniquely identify the user
     first_name = db.Column(db.String(50),nullable= False)
     last_name = db.Column(db.String(100),nullable=False)
     email = db.Column(db.String(100),nullable=False,unique=True)
     contact = db.Column(db.String(50),nullable=False, unique=True)
     password = db.Column(db.Text(),nullable=False)
     biography = db.Column(db.Text(100),nullable=True) 
     type = db.Column(db.String(20),nullable=False) # distinguishes the different types of users (admin manages the data)
     created_at =db.Column(db.DateTime,default= datetime.now())
     updated_at =db.Column(db.DateTime,onupdate= datetime.now())


 # creating the constructor for the  new instance author
     def __init__(self,first_name,last_name,email,contact,password,biography,type):
      super(Author,self).__init__()
      self.first_name = first_name
      self.last_name =last_name
      self.email = email
      self.contact = contact
      self.password = password
      self.biography =biography
      self.type = type

#  it helps to return a customised message
     def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

 
