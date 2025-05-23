from flask import Flask
from app.extensions import db,migrate,jwt
from app.controllers.auth.auth_controller import auth




# Apllication Function factory: it builds and returns an instance of a Flask application
def create_app():  # This is an application factory
    app = Flask(__name__)  # Initialize the Flask app
    app.config.from_object('config.Config')  # registering the database

    db.init_app(app)   # initialization on the app database
    migrate.init_app(app, db)# initialize flask-migrate
    jwt.init_app(app) # initialize the jwt

    # import the models
    from app.Models.authors import Author
    from app.Models.companies import Company
    from app.Models.books import Book



    app.register_blueprint(auth)




# register blueprints


    
   # migrations are always in order

    # Define routes
    @app.route("/")
    def home():
       return "Author's API setup"

    return app  # Return the app instance

# Only run the app if this script is executed directly
if  __name__ == '__main__':
  
    app = create_app()
    app.run(debug=True)  # Run the app
