from flask import Flask, jsonify, redirect, url_for, render_template, request,session, flash, send_file
import os
from werkzeug.datastructures import MultiDict
from Class_f import *
from decorator import *
from functions import *
from customer_blueprint import customer_b
from restaurant_blueprint import restaurant_b
from Restaurant import _restaurant

app = Flask(__name__, template_folder='templates')
app.secret_key = "tilhas6ise"
currentDirectory = os.path.abspath(__file__)
app.register_blueprint(customer_b, url_prefix='/customer')
app.register_blueprint(restaurant_b, url_prefix='/restaurant')


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

        success = registerManager.registerCustomer(firstname,lastname,email,username,password,confirmPassword,street,houseNr,plz)
        print(success)
        ##registering
        if success[0] == True:
            return redirect(url_for('registration_success'))
        else:
            flash(f"error : {success[1]}")
            return render_template("customer_register.html")
    
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
        print("login:", login)
        if login :##success
            session["user_id"] = login[0]
            session["username"] = username
            session["logged_in"] = True
            flash("login successfuly")
            print(session)
            return redirect(url_for("customer.home"))
        
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
            session["restaurant_id"] = login[0]
            session["email"] = login[1]
            session["username"] = login[2]
            #password = login[3]
            session["address"] = login[4]
            session["plz"] = login[5]
            session["restaurant_name"] = login[6]
            session["description"] = login[7]
            flash("login successfuly")
            return redirect(url_for('restaurant.restaurant_home')) 
        
        else:##failed
            flash("login failed check input")
            return render_template("restaurant_login.html")
    
    ##Linking "restaurant_login.html"
    else:
        return render_template("restaurant_login.html")
    
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
        
@app.route("/add_opening_time", methods = ["POST","GET"])
@login_required_restaurant
def add_opening_time():
    show_set_form = False
    show_add_form = True
    if request.method == "POST":
        form_data = MultiDict(request.form)
        #request restaurant id
        restaurant_id = session.get('restaurant_id')
        print("restautant id: ",restaurant_id)

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
            if plz not in postals and len(plz) == 5:
                postals.append(plz)
                print("added: ", postals)
            else:
                flash("enter a valid postal code")
            session['postals'] = postals

            return render_template('manage_plz.html', plz_list = postals)
        elif action == 'submit_postals':
            postals = session.get('postals')
            print(postals)
            if restaurant.add_plz(postals) == True:
                flash("delivery raduis updated successfuly")
                cleaned_postals = []
                session['postals'] = cleaned_postals
                return redirect(url_for('restaurant.restaurant_home'))
            else:
                flash("an error accured and raduis was not updated please try again")
                cleaned_postals = []
                session['postals'] = cleaned_postals
                return redirect(url_for('add_postal'))
    else:
       return render_template("manage_plz.html")

@app.route('/update_status', methods = ["POST"])
@login_required_restaurant
def update_status():#edit order status
      status = request.form['status']
      order_id = request.form.getlist('order_id')
      print(order_id)
      restaurant_id = session.get('restaurant_id')
      restaurant = _restaurant(restaurant_id,connection)
      for id in order_id:
        restaurant.update_order_status(id,status)
      return redirect(url_for('restaurant.restaurant_order'))

@app.route('/clear_history', methods = ['POST', 'GET'])
def clear_history():#clear history **testing for global
    id = session.get('user_id')
    user_type = request.form['user_type']
    
    if user_type == 'restaurant':
         id =session.get("restaurant_id")
    print(id,user_type)
    success = f.dlt_delivered(id,user_type)

    if success:
         if user_type == 'restaurant':
              return redirect(url_for("restaurant.restaurant_history"))
         else:
              return redirect(url_for('customer.home'))
    else:
         flash("failed to delete history")

@app.route('/clear_cart', methods=['POST'])
@login_required_customer
def clear_cart():#empty cart
    session.pop('cart_items', None)  # Remove the 'cart_items' key from the session
    flash('Cart cleared successfully', 'success')
    return redirect(url_for('order_cart.view_cart'))

#add logo

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/add_logo", methods=["POST", "GET"])
@login_required_restaurant
def add_logo():

    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    delivery_range = restaurant.get_delivery_raduis()

    if request.method == "POST":
        if 'logo' not in request.files:
            flash('No file part')
            return render_template("restaurant_home.html")
        
        logo_ = request.files['logo']
        if logo_.filename == '':
            flash('No selected file')
            return render_template("restaurant_home.html")

        if logo_ and allowed_file(logo_.filename):
            add = restaurant.updateRestaurantImage(logo_)
            #print("add:", add)
            if add:
                flash("Logo added successfully")
                updated_logo_data = restaurant.getLogo()
                print("updated logo: ", updated_logo_data)

                return redirect(url_for("restaurant.restaurant_home"))
            else:
                flash("Error occurred while adding the logo")
    return render_template("restaurant_home.html", show_menu_button=False, show_menu_form=True,range = delivery_range)

if __name__ == "__main__":
    app.run(debug=True)
    print("current directory:", currentDirectory)