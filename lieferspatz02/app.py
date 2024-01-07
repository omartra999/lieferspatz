import json
from flask import Flask, jsonify, redirect, url_for, render_template, request,session, flash
from werkzeug.datastructures import MultiDict
from RegistrationManager import registrationManager
from LoginManager import loginManager
from TimeManager import timeManager
from Restaurant import _restaurant
from PlzManager import plzManager
from datetime import datetime
from decorator import login_required_customer,login_required_restaurant
import sqlite3
from order_cart_blueprint import order_cart
from functions import f
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = "tilhas6ise"
currentDirectory = os.path.abspath(__file__)
connection = r"D:\\Study\\Sems 5\\Flask\\Lieferspatz.db"
app.register_blueprint(order_cart, url_prefix='/order_cart')


@app.route("/", methods = ["POST", "GET"])
def role():
    if request.method == "POST":
        ##requesting role
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
                session["restaurant_id"] = restaurant_id[1]
                session["logged_in_restaurant"] = True
                return redirect(url_for('add_opening_time',))
    
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

    ##login in
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        

        ##id check
        login = login_manager.loginCustomer(username, password)
        if login > 0:##success
            session["user_id"] = login
            session["username"] = username
            session["logged_in"] = True
            flash("login successfuly")
            print(session)
            return redirect(url_for("home"))
        
        else:##failed
            flash("login failed check input")
            return render_template("customer_login.html")
        
    ##Linking "customer_login.html"
    else:
        return render_template("customer_login.html")

@app.route("/restaurant_login", methods = ["POST","GET"])
def restaurant_login():
    login_manager = loginManager(connection)

    ##login in
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        ##id check
        login = login_manager.loginRestaurant(username, password)
        if login:##success
            session["logged_in_restaurant"] = True
            session["username"] = username
            restaurant_name = login[2]
            session["restaurant_name"] = restaurant_name
            restaurant_id = login[3]
            session["restaurant_id"] = restaurant_id
            address = login[4]
            session["address"] = address
            plz = login[5]
            session["plz"] = plz
            email = login[6]
            session["email"] = email
            description = login[7]
            session["description"] = description
            flash("login successfuly")
            return redirect(url_for('restaurant_home')) 
        
        else:##failed
            flash("login failed check input")
            return render_template("restaurant_login.html")
    
    ##Linking "restaurant_login.html"
    else:
        return render_template("restaurant_login.html")
    
@app.route("/restaurant_home", methods = ["POST","GET"])
@login_required_restaurant
def restaurant_home():
    restaurant_id = session['restaurant_id']
    time_manager = timeManager(connection)
    restaurant = _restaurant(restaurant_id, connection)
    if ('restaurant_name') in session and ('restaurant_id') in session:

        menu = restaurant.getMenu()
        delivery_range = restaurant.get_delivery_raduis()

        opening_times = time_manager.get_openning_times(restaurant_id)
        # Combine variables into a single dictionary
        template_data = {
        "restaurantName": session['restaurant_name'],
        "userName": session['username'],
        "restaurantAddress": session['address'],
        "Postal": session['plz'],
        "mail": session['email'],
        "des": session['description'],
        "should_show_edit_button": True,
        "show_menu_button": True,
        "items": menu,
        "range": delivery_range,
        "openTimes": opening_times
        # Add more variables as needed
        }
        print(template_data)
        return render_template("restaurant_home.html", **template_data)
    else:
        return redirect(url_for('restaurant_login'))

@app.route("/edit_restaurant_data", methods = ["POST","GET"])
@login_required_restaurant
def edit_restaurant_data():
    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    delivery_range = restaurant.get_delivery_raduis()
    if request.method == "POST":
        return render_template("restaurant_home.html", should_show_edit_form = True, should_show_edit_button = False, range = delivery_range)
    else:
        return redirect(url_for("restaurant_home"))
    
@app.route("/update_profile", methods = ["POST","GET"])
@login_required_restaurant
def update_profile():
    restaurant_id = session['restaurant_id']
    _restaurant_ = _restaurant(restaurant_id, connection) 
    if request.method == "POST":
        new_username = request.form.get('username')
        new_restaurant_name = request.form.get('restaurant_name')
        new_address = request.form.get('address')
        new_plz = request.form.get('plz')
        new_email = request.form.get('email')
        new_des = request.form.get('description')

        if new_username:
            _restaurant_.set_username(new_username)
            session['username'] = _restaurant_.get_username()
        if new_restaurant_name:
            _restaurant_.set_restaurant_name(new_restaurant_name)
            session['restaurant_name'] = _restaurant_.get_restaurant_name()
            print("new name: ", session['restaurant_name'])
        if new_address:
            _restaurant_.set_address(new_address)
            session['address'] = _restaurant_.get_address()
        if new_plz :
            _restaurant_.set_plz(new_plz)
            session['plz'] = _restaurant_.get_plz()
        if new_email:
            _restaurant_.set_email(new_email)
            session['email'] = _restaurant_.get_email()
        if new_des:
            _restaurant_.set_description(new_des)
            session['description'] = _restaurant_.get_description()
        flash("profile edited successfuly")
        return redirect(url_for('restaurant_home'))

    else:
        return url_for('edit_restaurant_data')

@app.route("/logout_restaurant", methods = ["POST","GET"])
@login_required_restaurant
def logout_restaurant():
    if request.method == "POST":
        session.pop('restaurant_name', None)
        session.pop('restaurant_id', None)
        session.pop('logged_in_restaurant', None)
        session.pop('username',None)

        return redirect(url_for('restaurant_login'))
    else:
        return redirect(url_for('restaurant_home'))
    
@app.route("/logout_customer", methods =["POST","GET"])
@login_required_customer
def logout_customer():
    if request.method == "POST":
        print(session)
        if 'cart_items' in session:
            flash("Cart is not clear. Please clear before you log out.")
            return redirect(url_for('order_cart.view_cart'))
        else:    
            session.clear()
            return redirect(url_for('login'))
    
#add open hours for a restaurant     
@app.route("/add_opening_time", methods = ["POST","GET"])
@login_required_restaurant
def add_opening_time():
    show_set_form = False
    show_add_form = True
    if request.method == "POST":
        form_data = MultiDict(request.form)
        #request restaurant id
        restaurant_id = session.get('restaurant_id')

        if not restaurant_id :
            flash("restaurant id not found please make sure you are logged in")
            return render_template("openning_times.html", should_show_add_form = show_add_form, should_show_set_form = show_set_form)
        
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
            return render_template('manage_plz.html', show_skip = True)
        else:
            flash("opening times were not added")
            return render_template("openning_times.html", should_show_add_form = show_add_form, should_show_set_form = show_set_form, show_skip = True)
    else:
        return render_template("openning_times.html", should_show_add_form = show_add_form, should_show_set_form = show_set_form, show_skip = True)

@app.route("/edit_opening_times", methods = ["POST","GET"])
@login_required_restaurant
def edit_opening_times():
    restaurant_id = session.get('restaurant_id')
    session['restaurant_id'] = restaurant_id
    print(restaurant_id)
    if request.method == "POST":
       return redirect(url_for('set_opening_times'))
    else:
        return render_template('restaurant_home.html')

@app.route("/set_opening_times", methods = ["POST","GET"])
@login_required_restaurant
def set_opening_times():
    show_add_form = False
    show_set_form = True
    restaurant_id = session.get('restaurant_id')
    print("id:",restaurant_id)
    if request.method == "POST":
        form_data = MultiDict(request.form)
        #request restaurant id
        if not restaurant_id :
            flash("restaurant id not found please make sure you are logged in")
            return render_template("openning_times.html", should_show_add_form = show_add_form, should_show_set_form = show_set_form)
        
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
        success = time_manager.set_openning_times(restaurant_id, days, open_times, close_times)
        if success:
            flash("opening times changed successfuly")
            return redirect(url_for('restaurant_home'))
        else:
            flash("please try again an error accured")
            return render_template("openning_times.html", should_show_add_form = show_add_form, should_show_set_form = show_set_form)
    else:
        return render_template("openning_times.html", should_show_add_form = show_add_form, should_show_set_form = show_set_form)




@app.route("/edit_menu", methods = ["POST","GET"])
@login_required_restaurant
def edit_menu():
    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id,connection)
    delivery_range = restaurant.get_delivery_raduis()

    if request.method == "POST":
        return render_template("restaurant_home.html",show_menu_button = False, show_menu_form = True, range = delivery_range )
    else:
        return url_for("restaurant_home")
        
@app.route("/delete_items", methods=["GET", "POST"])
@login_required_restaurant
def delete_items():
    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    if request.method == "POST":
        items_to_delete = request.form.getlist("items_to_delete")
        print(items_to_delete)
        for item in items_to_delete:
            if restaurant.delete_item(item_name=item):
                flash("Items deleted successfully")
            else:
                flash("an error accured")
        return redirect(url_for("restaurant_home"))

    items = restaurant.getMenu()  # Fetch menu items for display
    return render_template("delete_items.html", items=items)

@app.route("/delete_area", methods = ["POST", "GET"])
@login_required_restaurant
def delete_area():
    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    if request.method == "POST":
        areas_to_delete = request.form.getlist("areas_to_delete")
        print( "areas to delete:", areas_to_delete)
        if restaurant.delete_plz(areas_to_delete):
            flash("areas deleted successfully")
        else:
            flash("an error accured")
        return redirect(url_for("restaurant_home"))
    
##manage_plz omar version with no json, no list, single entries
@app.route('/add_postal', methods = ["POST","GET"])
@login_required_restaurant
def add_postal():
    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    postals = session.get('postals',[])
    if request.method == "POST":
        action = request.form.get('action')
        if action == "add_postal":
            plz = request.form.get('del_plz')      
            if len(plz) == 5:
                if plz not in postals:
                    postals.append(plz)
                    print("added: ", postals)
                else:
                    flash("Postal code already exists!")
            else:
                flash("Postal codes must have a length of 5 digits!") 
            session['postals'] = postals

            return render_template('manage_plz.html', plz_list = postals)
        elif action == 'submit_postals':
            postals = session.get('postals')
            print(postals)
            if restaurant.add_plz(postals) == True:
                flash("delivery raduis updated successfuly")
                cleaned_postals = []
                session['postals'] = cleaned_postals
                return redirect(url_for('restaurant_home'))
            else:
                flash("an error accured and raduis was not updated please try again")
                cleaned_postals = []
                session['postals'] = cleaned_postals
                return redirect(url_for('add_postal'))
    else:
       return render_template("manage_plz.html")

@app.route('/edit_range', methods = ["POST","GET"])
@login_required_restaurant
def edit_range():
    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    postals = restaurant.get_delivery_raduis()
    if request.method == "POST":
        return redirect(url_for('edit_range'))
    else:
        return render_template("edit_range.html", range = postals)

##manage_plz kawthar version using json to save plz as a list
@app.route('/manage_plz',methods = ["POST","GET"])
@login_required_restaurant
def manage_plz():
    restaurant_id = session.get('restaurant_id')
    plzList = []
    plz_manager = plzManager(connection)
    
    if request.method == 'POST':

        action = request.form.get('action')
        if action == 'add_plz_to_list':
            plz_value = request.form.get('plz')
            # Add the PLZ value to the list in the plz_manager instance
            plzList.append(plz_value)
            print("list: ", plzList)
            flash("PLZ added successfully")
            return render_template('manage_plz.html')

        elif action == 'submit_plz_list':
            plz_list_json = json.dumps(plzList)
            # If the user submitted without entering a PLZ, submit the existing PLZ list
            success = plz_manager.submit_plz_list(restaurant_id, plz_list_json)
            if success:
                flash("PLZ list submitted successfully")
                session['plzList'] = plzList
                plzList = []
                return render_template('manage_plz.html')
            else:
                flash("Failed to submit PLZ list")
                plzList = []
                return render_template('manage_plz.html')
            
    else:
        return render_template('manage_plz.html')



@app.route("/add_items", methods = ["POST", "GET"])
@login_required_restaurant
def add_items():

    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    if request.method == "POST":
      
        item_name = request.form.get('item_name')
        detail = request.form.get('detail')
        price = request.form.get('price')
        type = request.form.get('type')
        
        print("Item Name: ", item_name)
  
        if restaurant.add_item(item_name, detail, price, type):
            items = restaurant.getMenu()
            flash("item added successfuly")
            return render_template("restaurant_home.html", show_menu_button=False, show_menu_form=True, addedItems=items, range = restaurant.get_delivery_raduis())
        else:
            flash("Items are not added some Error occured")
            return render_template("restaurant_home.html", show_menu_button=False, show_menu_form=True)
    else:
        return render_template("restaurant_home.html", show_menu_button = False, show_menu_form = True)



@app.route("/home", methods=["GET", "POST"])
@login_required_customer
def home():
    
    if request.method == "GET":
        
        if "username" in session and "user_id" in session:  # login success
           

            conn = sqlite3.connect(connection)
            cursor = conn.cursor()

            # retrieving data
            cursor.execute("SELECT id, restaurantname, address, plz FROM restaurant")
            restaurants = cursor.fetchall()
            cursor.execute("SELECT restaurant_id, day, open, close FROM openning_times")
            openning_times = cursor.fetchall()
            cursor.execute("SELECT restaurant_id, item_name, price, detail, type FROM menu")
            menu = cursor.fetchall()
            conn.close()

            # Get the current day and time
            current_day = datetime.now().strftime("%A")
            current_time = datetime.now().strftime("%H:%M")
            # Filter out restaurants that are not open at the current time
            open_restaurants = []
            for restaurant in restaurants:
                for time in openning_times:
                    if restaurant[0] == time[0] and current_day.lower() == time[1].lower():
                        if time[2] <= current_time <= time[3]:
                            open_restaurants.append(restaurant)
                            break

            # Link home.html and all the restaurant
            return render_template("home.html", restaurants=open_restaurants, openning_times=openning_times, menus=menu, customer_id=session.get("user_id"))
        else:  # login failed
            return redirect(url_for("login"))
    elif request.method == "POST":
        # Handle POST request, e.g., form submission
        restaurant_id = request.form.get("restaurant_id")
        if restaurant_id:
            # Redirect to the restaurant_menu page with the selected restaurant_id
            return redirect(url_for("restaurant_menu", restaurant_id=restaurant_id))
        else:
            # Handle the case where restaurant_id is not provided
            flash("Invalid request. Please try again.")
            return redirect(url_for("home"))


@app.route("/restaurant_menu", methods=["POST", "GET"])
@login_required_customer
def restaurant_menu():
    
    if request.method == "POST":
        restaurant_id = request.form.get("restaurant_id")
        customer_id = request.form.get("customer_id")
        conn = sqlite3.connect(connection)  # Replace with your actual database file
        cursor = conn.cursor()
        

        # Fetch restaurant information based on the provided restaurant_id
        selected_restaurant = f.get_information(restaurant_id,'restaurant')

        cursor.execute("SELECT * FROM menu WHERE restaurant_id = ? ",(restaurant_id,))
        restaurantMenu = cursor.fetchall()

        conn.close()
        return render_template("restaurant_menu.html", restaurants=selected_restaurant, menus=restaurantMenu, customer_id=customer_id)
    else:  # login failed
            return redirect(url_for("login"))
        
 

@app.route("/delivery_timer")
def delivery_timer():
        return render_template("delivery_timer.html")






if __name__ == "__main__":
    app.run(debug=True)
    print("current directory:", currentDirectory)


