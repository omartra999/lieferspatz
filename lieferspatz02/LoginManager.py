import sqlite3

class loginManager:
    def __init__(self,connection):
        self.connection =sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def loginCustomer(self, username, password):
        customer_query = "SELECT * FROM customer WHERE username = ? AND password = ?"
        with self.connection:
            result = self.cursor.execute(customer_query, (username, password,)).fetchone()[0]
            return result 

    def loginRestaurant(self, username, password):
        restarant_query = "SELECT * FROM restaurant WHERE username = ? AND password = ?"
        with self.connection:
            result = self.cursor.execute(restarant_query, (username, password,)).fetchone()
            if result[0] > 0: 
                return result
            else: 
                return False
