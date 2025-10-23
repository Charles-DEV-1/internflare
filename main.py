from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, decode_token
import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)   
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # You can change this
jwt = JWTManager(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Index(Resource):
    def get(self):
        return {"message": "This is the Beginning of APIs"}
    
    def post(self):
        return {"message": "Posted"}


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # ✅ Correct logic: if any field is missing
        if not username or not email or not password:
            return jsonify({"message": "Fill all empty fields"}), 400
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message":"User already exists!"})
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # ✅ If all fields are present
        return jsonify({
            "Message": "User Created!",
            "User": {
                "username": username,
                "email": email,
                "password": password
            }
        }), 201

# To create the login page or route
class Login(Resource):
    # post: sending or creating something
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        #Checks if user is in the database
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return jsonify({"message":"Login successful!"})
        return jsonify({"message":"Invalid Credentials!"})
    
    #To create a route for users to request for password reset
class RequestPasswordReset(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message":"User not found!"})
        
        expires = datetime.timedelta(minutes=10)
        reset_token = create_access_token(identity=email, expires_delta=expires)

        reset_link = f"https://127.0.0.1/reset-link/{reset_token}"
        
        return jsonify({
            "message":"Password reset link has been sent to your email.",
            "reset_link": reset_link
        })
    

class ResetPassword(Resource):
    def post(self,token):
        try:
            decoded_token = decode_token(token)
            email = decoded_token["sub"]
        except Exception as e:
            return jsonify({"message":"Invalid or token expired!"}), 400
        data = request.get_json()
        new_password = data.get("new_password")

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        user.password = new_password
        db.session.commit()

        return jsonify({"message": "Password updated successfully!"}),200



api.add_resource(Login, "/login")
api.add_resource(SignUp, "/signup")
api.add_resource(Index, "/helloworld")
api.add_resource(RequestPasswordReset, "/forgot-password")
api.add_resource(ResetPassword, "/reset-password/<string:token>")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
