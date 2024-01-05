import sqlite3

class loginManager:
    def __init__(self,connection):
        self.connection =sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def loginCustomer(self, username, password):
        customer_query = "SELECT COUNT(*) FROM customer WHERE username = ? AND password = ?"
        with self.connection:
            result = self.cursor.execute(customer_query, (username, password,)).fetchone()[0]
            return result 

    def loginRestaurant(self, username, password):
        restarant_query = "SELECT COUNT(*), restaurantname, id, username, address, plz, email, description FROM restaurant WHERE username = ? AND password = ?"
        with self.connection:
            result = self.cursor.execute(restarant_query, (username, password,)).fetchone()
            auth = result[0]
            restaurant_name = result[1]
            restaurant_id = result[2]
            restaurant_username = result[3]
            restaurant_address = result[4]
            restaurant_plz = result[5]
            restaurant_email = result[6]
            restaurant_description = result[7]

            if auth > 0: 
                return auth, username, restaurant_name,restaurant_id,restaurant_address, restaurant_plz, restaurant_email, restaurant_description
            else: 
                return False