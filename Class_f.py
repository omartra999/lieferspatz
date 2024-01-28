import sqlite3
from datetime import datetime
from flask import Flask, request
from Restaurant import _restaurant
from functions import *
import json

class customer:
    
    #initialize f
    def __init__(self, customer_id, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()
        self.id = customer_id

    #show order
    def get_order(self):
        try:
            with self.connection:
                query = "SELECT * FROM Orders WHERE customer_id = ?"
                orders = self.cursor.execute(query, (self.id,)).fetchall()
                return orders
        except Exception as e:
            print(f"an error occured: {e}")
            return False 

    #submit order into database
    def add_to_cart(self, cart_items, item_id,item_name, price, restaurant_id):
        item_exists = False
        for item in cart_items:
            if item['item_id'] == item_id:
                item['quantity'] += 1
                item_exists = True
                break  # Exit loop if item is found

        if not item_exists:
            cart_items.append({
                'item_id': item_id,
                'restaurant_id': restaurant_id,
                'customer_id': self.id,
                'quantity': 1,
                'time': str(datetime.now().time().strftime('%H:%M')),
                'date': str(datetime.now().date()),
                'status': 'open',
                'description': ' ',
                'item_name': item_name,
                'price': price,
        })
        return cart_items

    #submit order from session
    def submit_order(self, cart_items):
        try:
            ##additional_description refers to the additional instructions textbox before the submit button
            additional_description = request.form.get('additional_description', '') 
            ##print(additional_description)
            query = "INSERT INTO Orders (item_id, restaurant_id, customer_id, quantity, time, date, status, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            for item in cart_items:
                parameters_order = (
                    item['item_id'],
                    item['restaurant_id'],
                    item['customer_id'],
                    item['quantity'],
                    item['time'],
                    item['date'],
                    item['status'],
                    additional_description,
                    )
                self.cursor.execute(query, parameters_order,)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"an error occured : {e}")
            return False

    #find restaurant(s) within range and time
    def get_available_restaurants(self):
        try:
            with self.connection:
                restaurants_query = "SELECT id, restaurantname, address, plz, description FROM restaurant"
                customer_plz_query = "SELECT plz FROM customer WHERE id = ?"
                opening_times_query = "SELECT restaurant_id, day, open, close FROM openning_times"
                menu_query = "SELECT restaurant_id, item_name, price, detail, types FROM menu"
                postal_query = "SELECT restaurant_id, plz FROM postal"
                menu = self.cursor.execute(menu_query).fetchall()
                restaurants = self.cursor.execute(restaurants_query).fetchall()
                opening_times = self.cursor.execute(opening_times_query).fetchall()
                customer_postal = self.cursor.execute(customer_plz_query, (self.id,)).fetchall()
                print("customer postal: ", customer_postal)
                delivery = self.cursor.execute(postal_query).fetchall()
                
                current_day = datetime.now().strftime("%A")
                current_time = datetime.now().strftime("%H:%M")
                
                open_restaurants = []
                for restaurant in restaurants:
                    for time in opening_times:
                        if restaurant[0] == time[0] and current_day.lower() == time[1].lower():
                            if time[2] <= current_time <= time[3]:
                                open_restaurants.append(restaurant)
                                print(f"Added restaurant {restaurant[1]} to open restaurants.")
                                break
              ##print(f"open_restaurants list before plz check(only time)-> {open_restaurants}")      

                filtered_restaurants = []
                logo = []

                for res in open_restaurants:
                    matching_entries = [entry for  entry in delivery if entry[0] == res[0] and entry[1] == customer_postal[0][0]]
                    if any(matching_entries):
                        filtered_restaurants.append(res)
                        print(f"Matching entries for restaurant {res[1]}: {matching_entries}")
                        logodata = _restaurant(matching_entries[0][0],connection).getLogo()
                        logo.append(logodata)

                open_restaurants = filtered_restaurants

                #print("open restaurants (after plz check): ", open_restaurants)

                return open_restaurants, opening_times, menu, logo
        except Exception as e:
            print(f"an error has occured: {e}")
            return False
        
class menuManager:
    
    #initial function
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
    
    ## check for replicated item name
    def item_exist(self,item_name):
        with self.connection:
            query = "SELECT COUNT(*) FROM menu WHERE item_name = ?" 
            result = self.connection.cursor().execute(query, (item_name,)).fetchone()[0]
            return result > 0
        
    ## create item into menu
    def create_item(self,restaurant,item_name,detail,price):
        with self.connection:
            query = "INSERT INTO menu(restaurant,item_name,detail,price) VALUES (? ,? ,?, ?)"
            parameter =(restaurant,item_name,detail,price)
            if self.item_exist(item_name):
                return False, "Item name exists, please change."
            else:
                with self.connection:
                    self.connection.cursor().execute(query, parameter)
                    return True, "item is added"
                
class loginManager:
    
    #initial
    def __init__(self,connection):
        self.connection =sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    #Customer login authorizor
    def loginCustomer(self, username, password):
        customer_query = "SELECT * FROM customer WHERE username = ? AND password = ?"
        with self.connection:
            result = self.cursor.execute(customer_query, (username, password,)).fetchone()
            return result 

    #Restaurant login authorizor
    def loginRestaurant(self, username, password):
        restarant_query = "SELECT * FROM restaurant WHERE username = ? AND password = ?"
        with self.connection:
            result = self.cursor.execute(restarant_query, (username, password,)).fetchone()
            return result
        
class plzManager:

    #initialize
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    #add plz into service
    def submit_plz_list(self, restaurant_id, plz_list):
        try:
            # Add the PLZ values from the list to the database
                with self.connection:
                    insert_query = "INSERT INTO restaurant_plz(restaurant_id, plz) VALUES (?, ?)"
                    self.cursor.execute(insert_query, (restaurant_id, plz_list,))
                self.connection.commit()
                return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    #show all available plz
    def get_plz_list(self, restaurant_id):
        query = "SELECT plz FROM restaurant_plz WHERE restaurant_id = ?"
        with self.connection:
            self.cursor.execute(query, (restaurant_id,))
            plz_list = [plz[0] for plz in self.cursor.fetchall()]
            return plz_list
        
class timeManager:
    
    #initialize
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    #show available day
    def dayExists(self, restaurant_id, day):
        try:
            with self.connection:
                query = "SELECT COUNT (*) FROM openning_times WHERE restaurant_id = ? AND day = ?"
                self.cursor.execute(query, restaurant_id, day,)
                count = self.cursor.fetchone()[0]
                return count > 0
        except Exception as e:
            print(f"an error accured: {e}")
            return False

    #add op time
    def add_openning_times(self, restaurant_id, days, opens, closes):
        print(f"extracted restaurant id form session : {restaurant_id}")
        try:
            with self.connection:
                insertQuery = "INSERT INTO openning_times(restaurant_id, day, open, close) VALUES (?,?,?,?)"
                for day, open, close in zip(days, opens, closes):
                    if self.dayExists(restaurant_id, day) == False:
                        exec = (restaurant_id, day, open, close,)
                        self.cursor.execute(insertQuery, (exec))
                    self.connection.commit()
                return True
        except Exception as e:
            print(f"An error accured: {e}")
            return False
                    
    #show op time                
    def get_openning_times(self, restaurant_id):
        query = "SELECT * FROM openning_times WHERE restaurant_id = ?"
        with self.connection:
            self.cursor.execute(query, (restaurant_id,))
            openning_times = self.cursor.fetchall()
            return openning_times

    #edit op time
    def set_openning_times(self, restaurant_id, days, opens, closes):
        print(f"extracted restaurant id form session : {restaurant_id}")
        try:
            #delete existing times
            with self.connection:
                deleteQuery = "DELETE FROM openning_times WHERE restaurant_id = ?"
                self.cursor.execute(deleteQuery, (restaurant_id,))
            
            #add the new times
            with self.connection:
                insertQuery = "INSERT INTO openning_times(restaurant_id, day, open, close) VALUES (?,?,?,?)"
                for day, open, close in zip(days, opens, closes):
                    if self.dayExists(restaurant_id, day) == False:
                        self.cursor.execute(insertQuery, (restaurant_id, day, open, close,))
                    self.connection.commit()

            return True
        except Exception as e :
            print(f"an error accured: {e}")
            return False
        
class registrationManager:
    
    #initial
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    #check if username exist
    def userNameExists(self, username):
        customer_query = "SELECT COUNT(*) FROM customer WHERE username = ?"        
        with self.connection:
            result = self.cursor.execute(customer_query, (username,)).fetchone()[0]
            return result > 0

    #check if restuarant exist    
    def restaurantExists(self, restaurant_name):
        restaurant_query = "SELECT COUNT(*) FROM restaurant WHERE restaurantname = ?"
        with self.connection:
            result = self.cursor.execute(restaurant_query, (restaurant_name,)).fetchone()[0]
            return result > 0

    #register customer
    def registerCustomer(self, firstname, lastname, email, username, password, passwordConfirm, street, houseNr, plz):
        customer_query = "INSERT INTO customer(firstname, lastname, email, username, password, street, houseNr, plz) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        parameters_customer = (firstname, lastname, email, username, password, street, houseNr, plz)

        if self.userNameExists(username):
            return False, "Username already exists"
        elif password != passwordConfirm:
            return False, "Passwords do not match" 
        else:
            with self.connection:
                self.cursor.execute(customer_query, parameters_customer)
                return True, "Customer added"

    #register restaurant
    def registerRestaurant(self, email, username, password, passwordConfirm, address, plz, restaurantname, description):
        restaurant_query = "INSERT INTO restaurant(email, username, password, address, plz, restaurantname, description) VALUES (?, ?, ?, ?, ?, ?, ?)"
        parameters_restaurant = (email, username, password, address, plz, restaurantname, description)

        if self.restaurantExists(username):
            return False, "Username already exists"
        elif password != passwordConfirm:
            return False, "Passwords do not match" 
        else:
            with self.connection:
                self.cursor.execute(restaurant_query, parameters_restaurant)
                #store the id
                restaurant_id = self.cursor.lastrowid
                self.addDefaultRestaurantLogo(restaurant_id) #here once the restau makes a registration, it get's a defult logo
                return True, restaurant_id
    
    #add default logo
    def addDefaultRestaurantLogo(self, restaurant_id):
        logo_query = "INSERT INTO restaurant_logo(restaurant_id, logo) VALUES (?, ?)"
        #default_logo_path = "C:\\Users\\kaouther\\Desktop\\DB Project\\static\\images\\r_logo.jpg"  #!!!guys don't forget to change the path when u update ur code

        with open(default_logo_path, 'rb') as default_logo_file:
            default_logo_data = default_logo_file.read()

        parameters_logo = (restaurant_id, default_logo_data)

        with self.connection:
            self.cursor.execute(logo_query, parameters_logo)