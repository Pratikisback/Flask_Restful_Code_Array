from main_project.register.views import User_Registration_Blueprint
from flask import Blueprint
from main_project import app

app.register_blueprint(User_Registration_Blueprint)
if __name__ == "__main__":
    app.run(debug=True)
