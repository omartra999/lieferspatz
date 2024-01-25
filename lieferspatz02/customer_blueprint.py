from flask import Blueprint, redirect, url_for, render_template, request,session, flash, jsonify
from werkzeug.datastructures import MultiDict
from Class_f import *
from decorator import *
from functions import *
from Restaurant import _restaurant

customer_b = Blueprint('customer', __name__)

@customer_b.route("/home", methods=["GET", "POST"])
@login_required_customer
def home():
    customer_id = session.get("user_id")
    _customer = customer(customer_id, connection)
    if request.method == "GET":
        open_restaurants = _customer.get_available_restaurants()[0]
        opening_times = _customer.get_available_restaurants()[1]
        menu = _customer.get_available_restaurants()[2]
        logo = _customer.get_available_restaurants()[3]


        return render_template("home.html", restaurants = open_restaurants, openning_times = opening_times, menus = menu, customer_id = customer_id, logo_data = logo)
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

@customer_b.route("/restaurant_menu", methods=["POST", "GET"])
@login_required_customer
def restaurant_menu():
    
    if request.method == "POST":
        restaurant_id = request.form.get("restaurant_id")
        customer_id = session.get("user_id")
        session["customer_id"] = customer_id
        #restaurant instance to retrieve the menu
        restaurant = _restaurant(restaurant_id, connection)
        _customer = customer(customer_id, connection)

        types_result = restaurant.get_item_types()
        types = [item_type[0] for item_type in types_result]
        menu_by_type = {}
        print("types: ", types)
        #sorting items with thier types in a dictionary
        for type in types:
            items = restaurant.get_items_of_type(type)
            menu_by_type[type] = []
            for item in items:
                menu_by_type[type].append({ "id": item[0], "restaurant_id":item[1] , "name":item[2], "description":item[3], "price": item[4], "logo": restaurant.getfoodLogo(item[0]) })
        menu = menu_by_type.items()
        
        print("menu:", menu)

        template_data = {
            "restaurant_name": restaurant.get_restaurant_name(),
            "description": restaurant.get_description(),
            "restaurant_adresse": restaurant.get_address(),
            "restaurant_plz": restaurant.get_plz(),
            "customer_id": customer_id,
            "customer_username": f.get_information(customer_id,"customer")[7],
            "menu": menu_by_type

            
        }
        

        return render_template("restaurant_menu.html", **template_data)
        # Fetch restaurant information based on the provided restaurant_id
    else:
        return redirect(url_for('home'))
    
@customer_b.route('/your_history', methods=['GET', 'POST'])
def customer_history():#show customer history
    print(session)
    conn = sqlite3.connect(connection)
    cursor = conn.cursor()

    user_type = request.form.get('user_type')
    id = session.get("user_id")
    
    if request.method == 'POST' and user_type:
        print(user_type)
        query = "SELECT * FROM Orders WHERE customer_id = ? AND Status = 'delivering' "
        history = cursor.execute(query, (id,)).fetchall()
        all_history = []
        print(history)
        if history:
            for p in history:
                template_data = {
                    "menu": f.get_information(p[1], 'menu'),
                    "restaurant": f.get_information(p[2], 'restaurant'),
                    "customer": f.get_information(p[3], 'customer'),
                    "history": p
                }
                all_history.append(template_data)
        print(all_history)
        return render_template("customer_history.html", all_history=all_history)
    else:
        return "No user type provided or invalid request."
    
@customer_b.route('/add_to_cart', methods=['POST'])
@login_required_customer
def add_to_cart():# add item into SESSION
 # Get item data from the AJAX request
    item_id = request.form.get('item_id')
    item_name = request.form.get('item_name')
    price = request.form.get('price')
    restaurant_id = request.form.get('restaurant_id')
    customer_id = session.get('user_id')
    _customer = customer(customer_id, connection)

    cart_items = session.get('cart_items', [])
    
    cart_items = _customer.add_to_cart(cart_items, item_id, item_name, price, restaurant_id)

    session['cart_items'] = cart_items
    # Return a response 
    return jsonify({'message': f'Item "{item_name}" added to the cart successfully!'})

@customer_b.route("/customer_cart", methods=["GET","POST"])
@login_required_customer
def view_cart():
    selected_status = request.form.get("order_status")
    # customer instance to retrieve the orders
    cart_items = session.get("cart_items", [])
    print("cart items:", cart_items)
    customer_id = session.get('user_id')
    _customer = customer(customer_id, connection)

    all_orders = _customer.get_order()

    #get total price
    total_price = f.get_total(cart_items)


     # Filter orders based on the selected status
    if (selected_status == "All") or (selected_status is None):
        filtered_orders = all_orders
    else:
        # If "All" is selected, show all orders
        filtered_orders = [order for order in all_orders if order[7] == selected_status]

    # Get the total price
    
    all_order = []
    if filtered_orders:
        for order in filtered_orders:
            #template data = [ menu information, restaurant information, customer_information, order_information]
            template_data = {
            "menu" : f.get_information(order[1],'menu'),
            "restaurant": f.get_information(order[2],'restaurant'),
            "customer": f.get_information(order[3],'customer'),
            "order" : order
            }
            all_order.append(template_data)
            
    # Pass the items to the HTML template
    return render_template("customer_cart.html", cart_items=cart_items,all_order = all_order,total_price ="{:.4}".format(total_price))

@customer_b.route('/filter_order', methods=['POST'])
@login_required_customer
def filter_orders():
     # Retrieve selected status from the form
    selected_status = request.form.get("order_status")

    # Retrieve all orders (replace this with your logic to get orders)
    customer_id = session.get('user_id')
    _customer = customer(customer_id, connection)
    all_orders = _customer.get_order()

    # Filter orders based on the selected status
    if selected_status != "All":
        filtered_orders = [order for order in all_orders if order[7] == selected_status]
    else:
        # If "All" is selected, show all orders
        filtered_orders = all_orders

    print("all_order:",all_orders)
    all_order = []
    if filtered_orders:
        for order in filtered_orders:
            #template data = [ menu information, restaurant information, customer_information, order_information]
            template_data = {
            "menu" : f.get_information(order[1],'menu'),
            "restaurant": f.get_information(order[2],'restaurant'),
            "customer": f.get_information(order[3],'customer'),
            "order" : order
            }
            all_order.append(template_data)
    # Pass the filtered orders to the template
    return render_template("customer_cart.html", all_order=all_order, cart_items=session.get("cart_items", []))

@customer_b.route('/submit_order', methods=['POST'])
@login_required_customer
def submit_order():#submit order from session into database
    print("reached submit order")
    # Retrieve items from session
    cart_items = session.get('cart_items', [])
    customer_id = session.get('customer_id')
    _customer = customer(customer_id, connection)
    if _customer.submit_order(cart_items):
    # Clear the cart after processing the items
        session.pop('cart_items', None)
    # Redirect to the home page after processing the order
        return redirect(url_for('customer.home'))
    else:
        flash("an error occured please try again")
        return redirect(url_for('order_cart.view_cart'))