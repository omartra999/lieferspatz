import sqlite3
from datetime import datetime
class customer:
    def __init__(self, customer_id, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()
        self.id = customer_id

    def get_order(self):
        try:
            with self.connection:
                query = "SELECT * FROM Orders WHERE customer_id = ?"
                orders = self.cursor.execute(query, (self.id,)).fetchall()
                return orders
        except Exception as e:
            print(f"an error occured: {e}")
            return False 

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
    def submit_order(self, cart_items):
        try:
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
                    item['description'],)
                self.cursor.execute(query, parameters_order,)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"an error occured : {e}")
            return False

    def get_available_restaurants(self):
        try:
            with self.connection:
                restaurants_query = "SELECT id, restaurantname, address, plz, description FROM restaurant"
                customer_plz_query = "SELECT plz FROM customer WHERE id = ?"
                opening_times_query = "SELECT restaurant_id, day, open, close FROM openning_times"
                menu_query = "SELECT restaurant_id, item_name, price, detail, type FROM menu"
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

                for res in open_restaurants:
                    matching_entries = [entry for  entry in delivery if entry[0] == res[0] and entry[1] == customer_postal[0][0]]
                    if any(matching_entries):
                        filtered_restaurants.append(res)
                        print(f"Matching entries for restaurant {res[1]}: {matching_entries}")

                
                open_restaurants = filtered_restaurants
                ##print("open restaurants (after plz check): ", open_restaurants)

                return open_restaurants, opening_times, menu
        except Exception as e:
            print(f"an error has occured: {e}")
            return False
        
        



        
