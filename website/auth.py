from flask import Blueprint, render_template, request, redirect, url_for
from db_manager import Database

auth = Blueprint('auth', __name__)

#Login Page
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db = Database()
        if db.validate_user_login(email,password):
            print("login success using the login page.")
            db.close()
            return redirect(url_for('auth.login'))
        else:
            print("login failed using the login page.")
            db.close()
            return redirect(url_for('auth.login'))

    return render_template("login.html")

#Logout Page
@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

#Register Page
@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        db = Database()
        data = db.fetch_data_from_a_page(page= "register")
        if data:
            db.create_table('employees') #will create it only if the table doesn't exist.
            db.insert_user_to_table('employees', data)
            db.close()
            return redirect(url_for('auth.login'))
    return render_template("register.html")

#forgot password Page
@auth.route('/forgotpass')
def forgotpass():
    return render_template("forgotpass.html")

#change password Page
@auth.route('/changepass', methods=['GET','POST'])
def changepass():

    if request.method == 'POST':
        email = request.form.get('email')
        old_password = request.form.get('oldPassword')
        new_password = request.form.get('newPassword')

        db = Database()
        db.change_password(email,old_password,new_password)
        db.close()
        return redirect(url_for('auth.login'))

    return render_template("changepass.html")

#change password Page
@auth.route('/randval')
def randval():
    return render_template("randval.html")

#add clients Page
@auth.route('/addclients', methods=['GET','POST'])
def addclient():
    db = Database()
    try:
        if request.method == 'POST':
            data = db.fetch_data_from_a_page(page= "addClients")
            if data:
                db.create_table('clients')
                db.insert_user_to_table('clients', data)
                return redirect(url_for('auth.addclient'))
    finally:
        db.close()
    return render_template("addClients.html")
