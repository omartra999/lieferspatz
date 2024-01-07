from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, request,session, flash, jsonify
from Restaurant import _restaurant
import sqlite3
from decorator import login_required_customer,login_required_restaurant
from functions import f
from Customer import customer

order_cart = Blueprint('order_cart', __name__)
connection = "C:\\Users\\User\\Desktop\\Uni\\lieferspatz-main\\lieferspatz02\\Lieferspatz.db"

@order_cart.route('/restaurant_order',  methods = ["POST","GET"])
@login_required_restaurant
def restaurant_order():#show restaurant open and accepted order
        conn = sqlite3.connect(connection)
        cursor = conn.cursor()

        #DB procedure
        open_query =  "SELECT * FROM Orders WHERE restaurant_id =  ? AND STATUS = 'open'" 
        restaurant_id = session.get('restaurant_id')
        open_orders = cursor.execute(open_query, (restaurant_id,)).fetchall()
        print("order[0]:",open_orders[0])
        #get all order information and sort it
        all_open_order = []
        if open_orders:
            for order in open_orders:
                    template_data = {
                    "menu": f.get_information(order[1], 'menu'),
                    "restaurant": f.get_information(order[2], 'restaurant'),
                    "customer": f.get_information(order[3], 'customer'),
                    "order": order
                    }
                    all_open_order.append(template_data)
        accepted_query =  "SELECT * FROM Orders WHERE restaurant_id =  ? AND (STATUS = 'accepted' OR STATUS = 'preparing')" 
        accepted_orders = cursor.execute(accepted_query, (restaurant_id,)).fetchall()
        all_accepted_order = []
        print("order[1]:",)
        if accepted_orders:
            for order in accepted_orders:
                    template_data = {
                    "menu": f.get_information(order[1], 'menu'),
                    "restaurant": f.get_information(order[2], 'restaurant'),
                    "customer": f.get_information(order[3], 'customer'),
                    "order": order
                    }
                    all_accepted_order.append(template_data)
        all_order = [all_open_order,all_accepted_order]
        print("orders:", all_order)
        return render_template("restaurant_cart.html",all_order = all_order, restaurant_id = restaurant_id)

@order_cart.route('/update_status', methods = ["POST"])
@login_required_restaurant
def update_status():#edit order status
      status = request.form['status']
      order_id = request.form['order_id']
      print(order_id)
      conn = sqlite3.connect(connection)
      cursor = conn.cursor()
      restaurant_id = session.get('restaurant_id')
      query = "UPDATE Orders SET status = ? WHERE id = ? AND restaurant_id = ?"
      cursor.execute(query, (status,order_id, restaurant_id,))
      conn.commit()
      cursor.close()
      conn.close()
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
        query = "SELECT * FROM Orders WHERE customer_id = ? AND Status = 'delivered' OR Status = 'delivering'"

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
        return render_template("history.html", all_history=all_history)
    else:
        return "No user type provided or invalid request."
    
@order_cart.route('/restaurant_history', methods=['GET', 'POST'])
def restaurant_history():#show restaurant history

    conn = sqlite3.connect(connection)
    cursor = conn.cursor()

    user_type = request.form.get('user_type')
    id = session.get("user_id")
    
    # show history 
    if request.method == 'POST':
        print(user_type)
        query = "SELECT * FROM Orders WHERE restaurant_id = ? AND Status = 'delivered' OR Status = 'delivering'"

        history = cursor.execute(query, (id,)).fetchall()
        all_history = []
        #same format as below
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
        return render_template("history.html", all_history=all_history)
    else:
        return "No user type provided or invalid request."


@order_cart.route('/clear_history', methods = ['POST', 'GET'])
def clear_history():#clear history **testing for global
      
      conn = sqlite3.connect(connection)
      cursor = conn.cursor()
      user_type =  request.form.get("user_type")
      id = session.get('restaurant_id')

      ##query = "DELETE FROM Orders WHERE " + user_type + "_id = ? AND STATUS ='delivered' " (testing if it can work)
      query = "DELETE FROM Orders WHERE restaurant_id = ? AND STATUS ='delivered' "
      cursor.execute(query, (id,))
      conn.commit()
      flash('History cleared successfully', 'success')
      cursor.close()
      conn.close()
      return redirect(url_for("restaurant_home"))

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
@order_cart.route("/customer_cart", methods=["GET"])
def view_cart():
    # customer instance to retrieve the orders
    cart_items = session.get("cart_items", [])
    customer_id = session.get('user_id')
    _customer = customer(customer_id, connection)

    orders = _customer.get_order()
    #create template
    all_order = []
    if orders:
        for order in orders:
            #template data = [ menu information, restaurant information, customer_information, order_information]
            template_data = {
            "menu" : f.get_information(order[1],'menu'),
            "restaurant": f.get_information(order[2],'restaurant'),
            "customer": f.get_information(order[3],'customer'),
            "order" : order
            }
            all_order.append(template_data)
    print(all_order)
    # Pass the items to the HTML template
    return render_template("customer_cart.html", cart_items=cart_items,all_order = all_order)


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