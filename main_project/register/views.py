from datetime import datetime, timedelta

import jwt
from flask import make_response, jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from main_project import api, Resource
from main_project.register.controller import add_user, find_user, update_Verify, update_password, remove_user
from main_project.register.utils import send_emails

User_Registration_Blueprint = Blueprint("Register_User", __name__)


class Register(Resource):
    def post(self):
        try:
            email = request.json.get("email")
            username = request.json.get("username")
            password = request.json.get("password")
            is_verified = False
            role = "Admin"
            new_user = {"email": email, "username": username, "password": password,
                        "is_verified": is_verified, "role": role}
            if not new_user:
                return make_response(jsonify({"Message": "Fill in the details"}))

            existing_user = find_user(email)
            if existing_user:
                return make_response(jsonify({"Message": "User already exists"}))
            try:
                token_expire_time = datetime.now() + timedelta(minutes=15)
                token_expire_time_epoch = int(token_expire_time.timestamp())

                payload = {"email": email, "exp": token_expire_time_epoch}
                print(payload)
                token = jwt.encode(payload, "zanc", algorithm="HS256")
                print(token)
                a = add_user(new_user)
                print(a)
                if send_emails(email, token):
                    return make_response(jsonify({"Message": "User registered successfully",
                                                  "username": username,
                                                  "email_id": email
                                                  }))
                else:
                    return make_response(jsonify({"Message": "Email not found"}))

            except Exception as e:
                return make_response(jsonify({"Message": str(e)}))

        except Exception as e:
            return make_response(jsonify({"Message": str(e)}))


class VerifyTheEmail(Resource):
    def post(self):
        try:
            # token = request.headers.get("authentication_key")
            token = request.headers.get('token')

            if token:
                token_dict = jwt.decode(token, "zanc", algorithms=["HS256"])
                email = token_dict[
                    "email"]  # We get the whole dictionary in token dict containing the email and the epoch time,
                # but we only need the email
                email_db = find_user(
                    email)  # Here we get the whole info on the email in db , to get the email we took the email from
                # the dictionary
                print(email)
                if email == email_db["email"]:
                    a = update_Verify(email)
                    print(a)
                return make_response(jsonify({"Message": "You can login now"}))
        except Exception as e:
            return make_response(jsonify({'Message': str(e)}))
        return make_response(jsonify({"Message": "Updated"}))


class Login(Resource):

    def post(self):
        # Credentials from API

        email = request.json.get("email")
        password = request.json.get("password")
        # Info from db as the dictionary will be returned in infodb we fetch the required values from the infodb for
        # validation
        infodb = find_user(email)
        if infodb in [None, " "]:
            return make_response(jsonify({'Message': "User not found or the password is wrong "}))
        emaildb = infodb["email"]
        passworddb = infodb["password"]
        is_verified = infodb["is_verified"]

        if is_verified:
            if email == emaildb and password == passworddb:
                access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))
                refresh_token = create_refresh_token(identity=email, expires_delta=timedelta(days=30))
                return make_response(jsonify({"Message": "You have logged in succesfully",
                                              "Access_token": access_token,
                                              "Refresh_token": refresh_token}))
            else:
                return make_response(jsonify({"Message": "Invalid credentials"}))
        else:
            return make_response(jsonify({"Message": "Your account is not verified"}))


class UpdateInfo(Resource):
    @jwt_required()
    def post(self):

        email = get_jwt_identity()
        current_password = request.json.get("current_password")
        new_password = request.json.get("new_password")
        info_db = find_user(email)
        passworddb = info_db["password"]
        if info_db["is_verified"]:
            if current_password == passworddb:
                update_password(email, new_password)
                return make_response(jsonify({"Message": "Password updated successfully"}))
            else:
                return make_response(jsonify({"Message": "Your password does not match with the current password"}))
        else:
            return make_response(jsonify({"Message": "Your account is not verified"}))


class RemoveUser(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        password = request.json.get("password")
        info_db = find_user(email)
        role = info_db["role"]
        if role == "Admin":
            if password == info_db["password"]:
                remove_user(email)
                return make_response(jsonify({"Message": "User has been deleted successfully and you cannot login "
                                                         "from this account now"}))
            else:
                return make_response(jsonify({"Message": "You don't have the authority to delete account"}))


api.add_resource(VerifyTheEmail, '/verify')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(UpdateInfo, '/updatepassword')
api.add_resource(RemoveUser, '/deleteuser')
