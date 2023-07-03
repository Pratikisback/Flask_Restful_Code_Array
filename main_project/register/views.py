from datetime import datetime, timedelta
from email.message import EmailMessage
from main_project.register.utils import send_emails
from main_project import app, api, Resource
from flask import make_response, jsonify, request, Blueprint
from main_project.register.controller import add_user, find_user, update_Verify
import smtplib
import jwt

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
                email = token_dict["email"]
                email_db = find_user(email)
                print(email)
                if email == email_db["email"]:
                    a = update_Verify(email)
                    print(a)
                return make_response(jsonify({"Message": "You can login now"}))
        except Exception as e:
            return make_response(jsonify({'Message': str(e)}))
        return make_response(jsonify({"Message": "Updated"}))


api.add_resource(VerifyTheEmail, '/verify')
api.add_resource(Register, '/register')
