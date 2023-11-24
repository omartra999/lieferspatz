from flask import Flask, redirect, url_for, render_template, request,session, flash
from RegistrationManager import registrationManager
from CustomerLogin import customerLogin
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "tilhas6ise"
currentDirectory = os.path.abspath(__file__)


@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        email = request.form["email"]
        street = request.form["street"]
        houseNr = request.form["houseNr"]
        plz = request.form["plz"]
        password = request.form["password"]
        confirmPassword = request.form["password_conformation"]
        
        session["firstname"] = firstname
        session["lastname"] = lastname
        session["username"] = username
        session["email"] = email
        session["street"] = street
        session["plz"] = plz
        session["houseNr"] = houseNr
        session["password"] = password
        session["confirmPassword"] = confirmPassword

        connection ="D:\\Uni Duisburg Essen\\DB\\lieferspatz02\\Lieferspatz.db"
        registerManager = registrationManager(connection)
        if registerManager.userNameExists(username):
            flash("username exists in database")
            return render_template("registration_form.html") 
        elif password != confirmPassword:
            flash("passwords do not match")
            return render_template("registration_form.html")
            
        elif registerManager.register(firstname,lastname,email,username,password,confirmPassword,street,houseNr,plz):
            return redirect(url_for('registration_success'))
    else:    
        return render_template("registration_form.html")


@app.route("/registration_success")
def registration_success():
    if "username" in session:
        username = session["username"]
        flash(f"{username} registered successfully")
        return redirect(url_for("login"))
    return redirect(url_for("register"))



@app.route("/login_customer", methods = ["POST","GET"])
def login():
    connection ="D:\\Uni Duisburg Essen\\DB\\lieferspatz02\\Lieferspatz.db"
    loginManager = customerLogin(connection)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if loginManager.login(username, password):
            session["username"] = username
            flash("login successfuly")
            return redirect(url_for("home"))
        else:
            flash("login failed check input")
            return render_template("login_customer.html")
    else:
        return render_template("login_customer.html")
@app.route("/home")
def home():
    if "username" in session:
        return render_template("home.html")
    else:
        return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)
    print(currentDirectory)
