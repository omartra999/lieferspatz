from flask import Flask, redirect, url_for, render_template, request,session
from RegistrationManager import registrationManager
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
        if registerManager.register(firstname,lastname,email,username,password,confirmPassword,street,houseNr,plz):
            return redirect(url_for('registration_success'))
        else:
            return redirect(url_for("registration_error"))
    else:    
        return render_template("registration_form.html")


@app.route("/registration_success")
def registration_success():
    if "username" in session:
        username = session["username"]
        return f"<h1>{username} registered successfully</h1>"
    return redirect(url_for("register"))

@app.route("/registration_error")
def registration_error():
    return f"<h1>Register failed<h1>"
     
if __name__ == "__main__":
    app.run(debug=True)
    print(currentDirectory)