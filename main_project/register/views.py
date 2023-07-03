from email.message import EmailMessage
from main_project.register.utils import send_emails
from main_project import app, api, Resource
from flask import make_response, jsonify, request, Blueprint
from main_project.register.controller import add_user, find_user
import smtplib

User_Registration_Blueprint = Blueprint("Register_User", __name__)


class Register(Resource):
    def post(self):
        try:
            email = request.json.get("email")
            username = request.json.get("username")
            password = request.json.get("password")
            is_verify = False
            role = "Admin"
            new_user = {"email": email, "username": username, "password": password,
                        "is_verify": is_verify, "role": role}
            if not new_user:
                return make_response(jsonify({"Message": "Fill in the details"}))

            existing_user = find_user(email)
            if existing_user:
                return make_response(jsonify({"Message": "User already exists"}))
            try:
                a = add_user(new_user)
                print(a)
                #To send email to the users registering
                # sender = "pratikgopal.cha26@gmail.com"
                # password = "svtitclscbvbxsai"
                # receiver = email
                # subject = "This is a test email"
                # body = """
                # This is the first attempt to send email using new method from a video
                # """
                #
                # em = EmailMessage()
                # em['From'] = sender
                # em['To'] = receiver
                # em['Subject'] = subject
                # em.set_content(body)
                #
                # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                #     smtp.login(sender, password)
                #     smtp.sendmail(sender, receiver, em.as_string())

                if send_emails(email):

                    return make_response(jsonify({"Message": "User registered successfully",
                                              "username": username,
                                              "email_id": email
                                              }))
                else:
                    return make_response(jsonify({"Message": "Email not found"}))

            except:
                return make_response(jsonify({"Message": "User was not added"}))

        except:
            return make_response(jsonify({"Message": "Info was not filled"}))


api.add_resource(Register, '/register')
