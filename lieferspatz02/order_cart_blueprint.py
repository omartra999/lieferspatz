from flask import Blueprint, redirect, url_for, render_template, request,session, flash
from Restaurant import _restaurant
import sqlite3
from decorator import login_required_customer,login_required_restaurant
from functions import f

order_cart = Blueprint('order_cart', __name__)
connection = "D:\\Study\\Sems 5\\Flask\\Lieferspatz.db"

@order_cart.route('/restaurant_order',  methods = ["POST","GET"])
@login_required_restaurant
def restaurant_order():#show restaurant open and accepted order
      conn = sqlite3.connect(connection)
      cursor = conn.cursor()
      open_query =  "SELECT item_id, restaurant_id, customer_id, quantity, time, date, status, description FROM Orders WHERE restaurant_id =  ? AND STATUS = 'open'" 
      restaurant_id = session.get('restaurant_id')
      open_orders = cursor.execute(open_query, (restaurant_id,)).fetchall()
      all_open_order = []
      if open_orders:
            for order in open_orders:
                  all_open_order.append(order)
                  break
      accepted_query =  "SELECT item_id, restaurant_id, customer_id, quantity, time, date, status, description FROM Orders WHERE restaurant_id =  ? AND STATUS = 'accepted'" 
      accepted_orders = cursor.execute(accepted_query, (restaurant_id,)).fetchall()
      all_accepted_order = []
      if accepted_orders:
            for order in accepted_orders:
                  all_accepted_order.append(order)
                  break
      return render_template("restaurant_cart.html",all_open_order = all_open_order, all_accepted_order = all_accepted_order)

@order_cart.route('/update_status', methods = ["POST"])
@login_required_restaurant
def update_status():#edit order status
      status = request.form['param_name']
      conn = sqlite3.connect(connection)
      cursor = conn.cursor()
      restaurant_id = session.get('restaurant_id')
      query = "UPDATE Orders SET status = ? WHERE restaurant_id = ?"
      cursor.execute(query, (status, restaurant_id,))
      conn.commit()
      cursor.close()
      conn.close()
      return redirect(url_for('order_cart.restaurant_order'))

@order_cart.route('/history', methods=['GET', 'POST'])
def history():
    print(session)
    conn = sqlite3.connect(connection)
    cursor = conn.cursor()

    user_type = request.form.get('user_type')
    id = session.get("user_id")
    
    if request.method == 'POST' and user_type:
        print(user_type)
        if user_type == 'restaurant':
            query = "SELECT * FROM Orders WHERE restaurant_id = ? AND Status = 'delivered' "
        elif user_type == 'customer':
            query = "SELECT * FROM Orders WHERE customer_id = ? AND Status = 'delivered' "
        else:
            return "Invalid user type or no user type provided."

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


@order_cart.route('/clear_history', methods = ['POST', 'GET'])
def clear_history():
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