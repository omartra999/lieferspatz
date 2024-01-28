from flask import Blueprint, redirect, url_for, render_template, request,session, flash, jsonify
from werkzeug.datastructures import MultiDict
from Class_f import *
from decorator import *
from functions import *
from Restaurant import _restaurant

restaurant_b = Blueprint('restaurant', __name__)

@restaurant_b.route("/restaurant_home", methods = ["POST","GET"])
@login_required_restaurant
def restaurant_home():
    restaurant_id = session['restaurant_id']
    time_manager = timeManager(connection)
    restaurant = _restaurant(restaurant_id, connection)
    if ('restaurant_name') in session and ('restaurant_id') in session:

        delivery_range = restaurant.get_delivery_raduis()
        opening_times = time_manager.get_openning_times(restaurant_id)
        logo_data = restaurant.getLogo()
        menu = restaurant.getMenu()
        items = []
        for item in menu:
            item_dic = {
                "item_id": item[0],
                "item_name": item[1],
                "item_description": item[2],
                "item_price": item[3],
                "item_type":item[4],
                "item_logo":restaurant.getfoodLogo(item[0])
            }
            items.append(item_dic)
        

       
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
            "items": items,
            "range": delivery_range,
            "openTimes": opening_times,
            "logo_data": logo_data
        }
        #print(template_data)
        return render_template("restaurant_home.html", **template_data)
    else:
        return redirect(url_for('restaurant_login'))
    
@restaurant_b.route("/edit_restaurant_data", methods = ["POST","GET"])
@login_required_restaurant
def edit_restaurant_data():
    restaurant_id = session.get('restaurant_id')
    time_manager = timeManager(connection)
    restaurant = _restaurant(restaurant_id, connection)
    delivery_range = restaurant.get_delivery_raduis()
    template_data = {
            "restaurantName": session['restaurant_name'],
            "userName": session['username'],
            "restaurantAddress": session['address'],
            "Postal": session['plz'],
            "mail": session['email'],
            "des": session['description'],
            "should_show_edit_button": False,
            "should_show_edit_form" : True,
            "show_menu_button": True,
            "items": restaurant.getMenu(),
            "range": delivery_range,
            "openTimes": time_manager.get_openning_times(restaurant_id),
            "logo_data": restaurant.getLogo()
        }
    if request.method == "POST":
        return render_template("restaurant_home.html",**template_data)
    else:
        return redirect(url_for("restaurant_home"),**template_data)

@restaurant_b.route("/update_profile", methods = ["POST","GET"])
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
            if len(new_plz) == 5:
                _restaurant_.set_plz(new_plz)
                session['plz'] = _restaurant_.get_plz()
            else:
                flash("enter a valid plz")
                return redirect(url_for('restaurant_home'))
        if new_email:
            _restaurant_.set_email(new_email)
            session['email'] = _restaurant_.get_email()
        if new_des:
            _restaurant_.set_description(new_des)
            session['description'] = _restaurant_.get_description()
           
        flash("profile edited successfuly")
        return redirect(url_for('restaurant_home'))

    else:
        return redirect(url_for('edit_restaurant_data'))
    
@restaurant_b.route("/edit_opening_times", methods = ["POST","GET"])
@login_required_restaurant
def edit_opening_times():
    restaurant_id = session.get('restaurant_id')
    session['restaurant_id'] = restaurant_id
    print(restaurant_id)
    if request.method == "POST":
       return redirect(url_for('restaurant.set_opening_times'))
    else:
        return render_template('restaurant_home.html')
    
@restaurant_b.route("/set_opening_times", methods = ["POST","GET"])
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
            return redirect(url_for('restaurant.restaurant_home'))
        else:
            flash("please try again an error accured")
            return render_template("openning_times.html", should_show_add_form = show_add_form, should_show_set_form = show_set_form)
    else:
        return render_template("openning_times.html", should_show_add_form = show_add_form, should_show_set_form = show_set_form)
    
@restaurant_b.route("/edit_menu", methods = ["POST","GET"])
@login_required_restaurant
def edit_menu():
    restaurant_id = session.get('restaurant_id')
    time_manager = timeManager(connection)
    restaurant = _restaurant(restaurant_id, connection)
    delivery_range = restaurant.get_delivery_raduis()
    menu = restaurant.getMenu()
    items = []
    for item in menu:
            item_dic = {
                "item_id": item[0],
                "item_name": item[1],
                "item_description": item[2],
                "item_price": item[3],
                "item_type":item[4],
                "item_logo":restaurant.getfoodLogo(item[0])
            }
            items.append(item_dic)

    template_data = {
            "restaurantName": session['restaurant_name'],
            "userName": session['username'],
            "restaurantAddress": session['address'],
            "Postal": session['plz'],
            "mail": session['email'],
            "des": session['description'],
            "show_menu_button": False,
            "show_menu_form" : True,
            "items": items,
            "range": delivery_range,
            "openTimes": time_manager.get_openning_times(restaurant_id),
            "logo_data": restaurant.getLogo()
        }
    
    if request.method == "POST":
        return render_template("restaurant_home.html", **template_data )
    else:
        return url_for("restaurant_home")
    
@restaurant_b.route("/delete_items", methods=["GET", "POST"])
@login_required_restaurant
def delete_items():
    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    if request.method == "POST":
        items_to_delete = request.form.getlist("items_to_delete")
        for item in items_to_delete:
            if restaurant.delete_item(item):
                flash("Items deleted successfully")
            else:
                flash("an error accured")
        return redirect(url_for("restaurant_home"))

    items = restaurant.getMenu()  # Fetch menu items for display
    print("menu: ", items)
    all_menu = []
    for item in items:
        menu = {
            "items":item,
            "logo":restaurant.getfoodLogo(item[0])
        }
        all_menu.append(menu)
        
    return render_template("delete_items.html", all_menu= all_menu)

@restaurant_b.route("/delete_area", methods = ["POST", "GET"])
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
        return redirect(url_for("restaurant.restaurant_home"))
 
@restaurant_b.route('/edit_range', methods = ["POST","GET"])
@login_required_restaurant
def edit_range():
    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    postals = restaurant.get_delivery_raduis()
    if request.method == "POST":
        return redirect(url_for('restaurant.edit_range'))
    else:
        return render_template("edit_range.html", range = postals)

@restaurant_b.route("/add_items", methods = ["POST", "GET"])
@login_required_restaurant
def add_items():
    time_manager = timeManager(connection)
    restaurant_id = session.get('restaurant_id')
    restaurant = _restaurant(restaurant_id, connection)
    if request.method == "POST":
      
        item_name = request.form.get('item_name')
        detail = request.form.get('detail')
        price = request.form.get('price')
        types = request.form.get('types')
        logo = request.files.get('food_logo')
        print("logo:",logo)
        
        
        
        if restaurant.add_item(item_name, detail, price, types, logo):
            items = restaurant.getMenu()
            flash("item added successfuly")
            template_data = {
            "restaurantName": session['restaurant_name'],
            "userName": session['username'],
            "restaurantAddress": session['address'],
            "Postal": session['plz'],
            "mail": session['email'],
            "des": session['description'],
            "should_show_edit_button": False,
            "should_show_edit_form" : False,
            "show_menu_button": False,
            "show_menu_form":True,
            "addedItems": restaurant.getMenu(),
            "range":  restaurant.get_delivery_raduis(),
            "openTimes": time_manager.get_openning_times(restaurant_id),
            "logo_data": restaurant.getLogo()
        }
            return render_template("restaurant_home.html", **template_data)
        else:
            flash("Items are not added some Error occured")
            return render_template("restaurant_home.html", show_menu_button=False, show_menu_form=True)
    else:
        return render_template("restaurant_home.html", show_menu_button = False, show_menu_form = True)

@restaurant_b.route('/restaurant_order',  methods = ["POST","GET"])
@login_required_restaurant
def restaurant_order():#show restaurant open and accepted order
        
        restaurant_id = session.get('restaurant_id')
        restaurant = _restaurant(restaurant_id, connection)
        open_orders = restaurant.get_open_orders()
        accepted_orders = restaurant.get_accepted_orders()
        #get all order information and sort it
        open_order_by = {}
        if open_orders:
            for order in open_orders:
                    customer_name = f.get_information(order[3], 'customer')[7]
                    if customer_name not in open_order_by:
                         open_order_by[customer_name] = []
                    
                    template_data = {
                    "menu": f.get_information(order[1], 'menu'),
                    "restaurant": f.get_information(order[2], 'restaurant'),
                    "customer": f.get_information(order[3], 'customer'),
                    "order": order
                    }
                    open_order_by[customer_name].append(template_data)

        
        accepted_order_by = {}
        if accepted_orders:
            for order in accepted_orders:
                    customer_name = f.get_information(order[3], 'customer')[7]
                    if customer_name not in accepted_order_by:
                         accepted_order_by[customer_name] = []
                    
                    template_data = {
                    "menu": f.get_information(order[1], 'menu'),
                    "restaurant": f.get_information(order[2], 'restaurant'),
                    "customer": f.get_information(order[3], 'customer'),
                    "order": order
                    }
                    accepted_order_by[customer_name].append(template_data)
        #print("accepted:",accepted_order_by)
        all_order = [open_order_by,accepted_order_by]
        #print("orders:", all_order)
        return render_template("restaurant_cart.html",all_order = all_order, restaurant_id = restaurant_id)

@restaurant_b.route('/restaurant_history', methods=['GET', 'POST'])
def restaurant_history():#show restaurant history

    restaurant_id = session.get("restaurant_id")
    #print("restaurant_id:", restaurant_id)
    restaurant = _restaurant(restaurant_id, connection)    
    # show history 
    if request.method == 'GET':
        history = restaurant.get_order_history()
        all_history = []
        #same format as below
        if history:
            for p in history:
                template_data = {
                    "menu": f.get_information(p[1], 'menu'),
                    "restaurant": f.get_information(p[2], 'restaurant'),
                    "customer": f.get_information(p[3], 'customer'),
                    "status": p[7],
                    "history": p
                }
                all_history.append(template_data)
        print(all_history)
        return render_template("restaurant_history.html", all_history=all_history)
    else:
        return "No user type provided or invalid request."

