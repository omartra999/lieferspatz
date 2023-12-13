from flask import Flask, redirect, url_for, render_template, request,session, flash
from werkzeug.datastructures import MultiDict
from RegistrationManager import registrationManager
from LoginManager import loginManager
from MenuManager import menuManager
from TimeManager import timeManager
import sqlite3
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = "tilhas6ise"
currentDirectory = os.path.abspath(__file__)
connection = "D:\\Uni Duisburg Essen\\DB\\lieferspatz02\\Lieferspatz.db"

@app.route("/", methods = ["POST", "GET"])
def role():
    if request.method == "POST":
        ##requesting  role
        selected_role = request.form['role']

        ##redirecting to according URL
        if selected_role == "customer":
            return redirect(url_for("register"))
        
        elif selected_role == "restaurant":
            return redirect(url_for("restaurant_register"))
        
        else: 
            return "ERROR"
    
    ##Linking "index.html"
    else:
       return render_template("index.html")
    

@app.route("/register", methods = ["POST", "GET"])
def register():
    registerManager = registrationManager(connection)
    if request.method == "POST":
        ## role set
        user_type = "customer"
        ## request from html
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        email = request.form["email"]
        street = request.form["street"]
        houseNr = request.form["houseNr"]
        plz = request.form["plz"]
        password = request.form["password"]
        confirmPassword = request.form["password_conformation"]
        
        #temporarily store input
        session["firstname"] = firstname
        session["lastname"] = lastname
        session["username"] = username
        session["email"] = email
        session["street"] = street
        session["plz"] = plz
        session["houseNr"] = houseNr
        session["password"] = password
        session["confirmPassword"] = confirmPassword
        session["usertype"] = "customer"


        ##comfirming password 
        if password != confirmPassword:
            flash("passwords do not match")
            return render_template("customer_register.html")
        
        ##registering
        elif registerManager.registerCustomer(firstname,lastname,email,username,password,confirmPassword,street,houseNr,plz):
            return redirect(url_for('registration_success'))
    
    ##linking to "customer_register.html" 
    else:
        return render_template("customer_register.html")

@app.route("/restaurant_register", methods = ["POST", "GET"])
def restaurant_register():
    registerManager = registrationManager(connection)
    if request.method == "POST":
            
        ## request from html
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirmPassword = request.form["password_conformation"]
        address = request.form["address"]
        plz = request.form["plz"]
        restaurantname = request.form["restaurantname"]
        description = request.form["description"]
        
        #temporarily store input
        session["email"] = email
        session["username"] = username
        session["password"] = password
        session["confirmPassword"] = confirmPassword
        session["address"] = address
        session["plz"] = plz
        session["restaurantname"] = restaurantname
        session["description"] = description

        restaurant_id = registerManager.registerRestaurant(email, username, password, confirmPassword, address, plz, restaurantname, description)


        ##comfirming password 
        if password != confirmPassword:
            flash("passwords do not match")
            return render_template("restaurant_register.html")
        
        ##registering and retrive restaurant id from the database
        elif restaurant_id is not None:
                #store the id
                session["restaurant_id"] = restaurant_id
                return redirect(url_for('add_opening_time'))
    
    ##Linking "restaurant_register.html"
    else:    
        return render_template("restaurant_register.html")

@app.route("/registration_success")
def registration_success():
    
    if "username" in session:  ##login success

        username = session["username"]

        #flasing "registered successfully" with username
        flash(f"{username} registered successfully")

        #redirecting to login
        return redirect(url_for("login"))
    
    return redirect(url_for("register")) #login failed

@app.route("/login", methods = ["POST","GET"])
def login():
    login_manager = loginManager(connection)

    ##role set
    role="customer"


    ##login in
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        ##id check
        if login_manager.login(username, password,role):##success
            session["username"] = username
            flash("login successfuly")
            return redirect(url_for("home"))
        
        else:##failed
            flash("login failed check input")
            return render_template("customer_login.html")
        
    ##Linking "customer_login.html"
    else:
        return render_template("customer_login.html")

@app.route("/restaurant_login", methods = ["POST","GET"])
def restaurant_login():

    ##role set
    role ="restaurant"

    login_manager = loginManager(connection)

    ##login in
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        ##id check
        if login_manager.login(username, password,role):##success
            session["username"] = username
            flash("login successfuly")
            return redirect(url_for("it_work"))                                 ##NOT DONE
        
        else:##failed
            flash("login failed check input")
            return render_template("restaurant_login.html")
    
    ##Linking "restaurant_login.html"
    else:
        return render_template("restaurant_login.html")
    
#add open hours for a restaurant     
@app.route("/add_opening_time", methods = ["POST","GET"])
def add_opening_time():
    if request.method == "POST":
        form_data = MultiDict(request.form)
        #request restaurant id
        restaurant_id = session.get('restaurant_id')

        if not restaurant_id :
            flash("restaurant id not found please make sure you are logged in")
            return render_template("openning_times.html")
        
        days = []
        open_times = []
        close_times = []

    # Loop through form data and extract values based on keys containing 'days[', 'open_time[', 'close_time['
        for key, value in form_data.items():
            if key.startswith('days['):
                days.append(value)
            elif key.startswith('open_time['):
                open_times.append(value)
            elif key.startswith('close_time['):
                close_times.append(value)

        print("raw entered data: " ,restaurant_id,days,open_times,close_times)
        time_manager = timeManager(connection)
        success = time_manager.add_openning_times(restaurant_id, days, open_times, close_times)
        if success:
            flash("opening times added successfuly")
            return render_template("openning_times.html")
        else:
            flash("opening times were not added")
            return render_template("openning_times.html")
    else:
        return render_template("openning_times.html")

@app.route("/home")
def home():

    if "username" in session: ## login success

        conn = sqlite3.connect(connection)
        cursor = conn.cursor()

        ##retrieveing data
        cursor.execute("SELECT restaurantname, address, plz FROM restaurant")
        restaurants = cursor.fetchall()
        conn.close()

        ##Link home.html and all the restaurant
        return render_template("home.html",restaurants=restaurants)
    
    else: ## login failed
        return redirect(url_for("login"))

@app.route('/restaurant/<string:restaurant_id>')
def restaurant(restaurant_id):

    conn = sqlite3.connect(connection)
    cursor = conn.cursor()

    ##fetch restaurant info
    cursor.execute("SELECT * FROM restaurant WHERE username=?", (restaurant_id,))
    restaurant_info = cursor.fetchone()

    ##fetch menu
    cursor.execute("SELECT * FROM menu WHERE restaurant=?", (restaurant_id,))
    menu = cursor.fetchall()
    conn.close()

    ##getting info
    if restaurant_info:
        ##columns are in order: id[0], first_name[1], last_name[2],street[3],houseNr[4]
        ##plz[5], email[6], username[7], password[9]
        restaurant = {
            'id': restaurant_info[0],
            'first_name': restaurant_info[1],
            'last_name': restaurant_info[2],
            'street': restaurant_info[3],
            'houseNr': restaurant_info[4],
            'plz':restaurant_info[5],
            'email':restaurant_info[6],
            'username':restaurant_info[7],
            'menu':menu
            # Add more columns if needed
        }
        return render_template('restaurant.html', restaurant=restaurant)
    else:
        return "Restaurant not found."




##temp create menu for testing
@app.route("/create_menu/<string:restaurant_id>", methods = ["POST", "GET"])
def create_menu(restaurant_id):

    if request.method == "POST":

        ## request from html
        item_name = request.form["item_name"]
        detail = request.form["detail"]
        price = request.form["price"]
        
        #temporarily store input
        session["item_name"] = item_name
        session["detail"] = detail
        session["price"] = price
        
        menu = menuManager(connection)

        ##checking unique username
        if menu.item_exist(item_name):
            flash("item exists")
            return render_template("create_item.html", restaurant=restaurant_id)
        
        
        ##registering
        elif menu.create_item(restaurant_id,item_name, detail, price):
            return redirect(url_for("restaurant", restaurant_id=restaurant_id))
    
    ##linking to "customer_register.html" 
    else:
        return render_template("create_item.html",restaurant=restaurant_id)

##testing
@app.route("/it_work")
def it_work():
    return render_template("create_menu.html")  

  
if __name__ == "__main__":
    app.run(debug=True)
    print(currentDirectory)
