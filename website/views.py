from flask import Blueprint, render_template, request



views = Blueprint('views', __name__)

#Home Page
@views.route('/')
def home():
    return render_template("home.html")





