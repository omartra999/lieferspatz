import sqlite3

class loginManager:
    def __init__(self,connection):
        self.connection =sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def login(self, username, password,role):
        customer_query = "SELECT COUNT(*) FROM customer WHERE username = ? AND password = ?"
        restaurant_query = "SELECT COUNT(*) FROM restaurant WHERE username = ? AND password = ?"
        with self.connection:
            if role == "customer":
                result = self.cursor.execute(customer_query,(username, password,)).fetchone()[0]
            if role == "restaurant":
                result = self.cursor.execute(restaurant_query,(username, password,)).fetchone()[0]       
            if result > 0:
                return True
    ##add a restaurant log in function to also return boolean
