# authentication process of author regitration ,it stores all the function
from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
import validators
from app.Models.authors import Author
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# autth blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# user registeration
@auth.route('/register', methods=['POST'])
def register_author():  # controllers use function
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    contact = data.get('contact')
    password = data.get('password')
    type = data.get('type', 'author')
    biography = data.get('biography', '') if type == "author" else ''

    # validations of the incoming request
    if not first_name or not last_name or not contact or not password or not email:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    if type == 'author' and not biography:
        return jsonify({"error": "Enter your author biography"}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({"error": "password is too short"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({"errors": "Email is not vaild"}), HTTP_400_BAD_REQUEST

    if Author.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email address in use"}), HTTP_409_CONFLICT

    if Author.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error": "Contact already in use"}), HTTP_409_CONFLICT

    try:
        hashed_password = bcrypt.generate_password_hash(password)  # hashed password
        # creating new author
        new_author = Author(first_name=first_name, last_name=last_name, password=hashed_password,
                            email=email, contact=contact, type=type, biography=biography)
        db.session.add(new_author)
        db.session.commit()

        # authorname
        authorname = new_author.get_full_name()

        return jsonify({
            'message': f"{authorname} has been successfully created as an {new_author.type}",
            'user': {
                "id": new_author.id,
                "first_name": new_author.first_name,
                "last_name": new_author.last_name,
                "email": new_author.email,
                "type": new_author.type,
                "biography": new_author.biography,
                "created_at": new_author.created_at,
            }

        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# author login based on their identity
# use the method post
@auth.post('/login')
def login():
    # use email when longinig in the author
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        if not password or not email:
            return jsonify({'message': "Email and password are required"}), HTTP_400_BAD_REQUEST

        author = Author.query.filter_by(email=email).first()

        if author:
            Is_correct_password = bcrypt.check_password_hash(author.password, password)
            refresh_token = create_access_token(identity=author.id, fresh=False)

            if Is_correct_password:
                # they must be unique
                access_token = create_access_token(identity=author.id, fresh=True)

                return jsonify({
                    'author': {
                        'id': author.id,
                        'username': author.get_full_name(),
                        'email': author.email,
                        'acess_token': access_token,
                        'refresh_token': refresh_token,
                        'type': author.type
                    },
                    'message': "You have successfully logged into your account"
                }), HTTP_200_OK

            else:
                return jsonify({'message': "Invalid password"}), HTTP_401_UNAUTHORIZED

        else:
            return jsonify({'message': "Invalid email address"}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update the refresh token endpoint to use POST method consistently
@auth.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}),HTTP_200_OK
