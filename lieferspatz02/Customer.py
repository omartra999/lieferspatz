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
        
        



        