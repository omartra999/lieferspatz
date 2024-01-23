from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, request,session, flash, jsonify
from Restaurant import _restaurant
import sqlite3
from decorator import login_required_customer,login_required_restaurant
from functions import f,connection
from Customer import customer
from Restaurant import _restaurant

order_cart = Blueprint('order_cart', __name__)


@order_cart.route('/restaurant_order',  methods = ["POST","GET"])
@login_required_restaurant
def restaurant_order():#show restaurant open and accepted order
        
        restaurant_id = session.get('restaurant_id')
        restaurant = _restaurant(restaurant_id, connection)
        open_orders = restaurant.get_open_orders()
        #get all order information and sort it
        all_open_order = []
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

        
        accepted_orders = restaurant.get_accepted_orders()
        all_accepted_order = []
        if accepted_orders:
            for order in accepted_orders:
                    template_data = {   
                    "menu": f.get_information(order[1], 'menu'),
                    "restaurant": f.get_information(order[2], 'restaurant'),
                    "customer": f.get_information(order[3], 'customer'),
                    "order": order
                    }
                    all_accepted_order.append(template_data)
        all_order = [open_order_by,all_accepted_order]
        #print("orders:", all_order)
        return render_template("restaurant_cart.html",all_order = all_order, restaurant_id = restaurant_id)
    
@order_cart.route('/update_status', methods = ["POST","GET"])
@login_required_restaurant
def update_status():#edit order status
      status = request.form['status']
      order_id = request.form.getlist['order_id']
      print("all_order_id:",order_id)
      restaurant_id = session.get('restaurant_id')
      restaurant = _restaurant(restaurant_id,connection)
      #for that_id in order_id:
      #  restaurant.update_order_status(that_id,status)
      return redirect(url_for('order_cart.restaurant_order'))

@order_cart.route('/your_history', methods=['GET', 'POST'])
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
    
@order_cart.route('/restaurant_history', methods=['GET', 'POST'])
def restaurant_history():#show restaurant history

    restaurant_id = session.get("restaurant_id")
    print("restaurant_id:", restaurant_id)
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


@order_cart.route('/clear_history', methods = ['POST', 'GET'])
def clear_history():#clear history **testing for global
    id = session.get('user_id')
    user_type = request.form['user_type']
    
    if user_type == 'restaurant':
         id =session.get("restaurant_id")
    
    success = f.dlt_delivered(id,user_type)

    if success:
         if user_type == 'restaurant':
              return redirect(url_for("order_cart.restaurant_history"))
         else:
              return redirect(url_for('home'))
    else:
         flash("failed to delete history")

@order_cart.route('/add_to_cart', methods=['POST'])
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

    
## this one is for viewing the cart
@order_cart.route("/customer_cart", methods=["GET","POST"])
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


@order_cart.route('/clear_cart', methods=['POST'])
def clear_cart():#empty cart
    session.pop('cart_items', None)  # Remove the 'cart_items' key from the session
    flash('Cart cleared successfully', 'success')
    return redirect(url_for('order_cart.view_cart'))

@order_cart.route('/clear_order', methods=['POST'])
@login_required_customer
def clear_order():#delete history
    conn = sqlite3.connect(connection)
    cursor = conn.cursor()
    customer_id = session.get("user_id")
    cursor.execute("DELETE FROM Orders WHERE customer_id = ?", (customer_id,))
    conn.commit()
    flash('Order cleared successfully', 'success')
    cursor.close()
    conn.close()
    return redirect(url_for('view_cart'))


@order_cart.route('/submit_order', methods=['POST'])
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
        return redirect(url_for('home'))
    else:
        flash("an error occured please try again")
        return redirect(url_for('order_cart.view_cart'))
    