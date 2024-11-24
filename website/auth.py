
from flask import Blueprint, render_template, request


auth = Blueprint('auth', __name__)


#Login Page
@auth.route('/login')
def login():
    return render_template("login.html")

#Logout Page
@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

#Register Page
@auth.route('/register')
def register():
    return render_template("register.html")

#forgot password Page
@auth.route('/forgotpass')
def forgotpass():
    return render_template("forgotpass.html")

#change password Page
@auth.route('/changepass')
def changepass():
    return render_template("changepass.html")

#change password Page
@auth.route('/randval')
def randval():
    return render_template("randval.html")
