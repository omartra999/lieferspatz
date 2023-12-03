import sqlite3

class registrationManager:
    
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
    def userNameExists(self, username):
        with self.connection:
            customer_query = "SELECT COUNT(*) FROM customer WHERE username = ?"
            restaurant_query = "SELECT COUNT(*) FROM restaurant WHERE username = ?"
            result1 = self.connection.cursor().execute(customer_query, (username,)).fetchone()[0]
            result2 = self.connection.cursor().execute(restaurant_query, (username,)).fetchone()[0]
            return (result1 > 0 or result2 > 0)
    
    def register(self, firstname, lastname, email, username, password,passwordConfirm, street, houseNr, plz,user_type):
            cursor = self.connection.cursor()
            customer_query = "INSERT INTO customer(firstname, lastname, email, username, password, street, houseNr, plz) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            restaurant_query = "INSERT INTO restaurant(firstname, lastname, email, username, password, street, houseNr, plz) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            parameters = (firstname, lastname, email, username, password, street, houseNr, plz)
            if self.userNameExists(username):
                return False, "username already exists"
            
            elif password != passwordConfirm:
              return False, "passwords do not match" 
            else:
                with self.connection:
                    if user_type == "customer":
                        cursor.execute(customer_query, parameters)
                        return True, "customer added"
                    elif user_type == "restaurant":
                        cursor.execute(restaurant_query, parameters)
                        return True, "restaurant added"
                    

