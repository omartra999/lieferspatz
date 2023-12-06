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
    
    def registerCustomer(self, firstname, lastname, email, username, password,passwordConfirm, street, houseNr, plz):
            cursor = self.connection.cursor()
            customer_query = "INSERT INTO customer(firstname, lastname, email, username, password, street, houseNr, plz) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            parameters_customer = (firstname, lastname, email, username, password, street, houseNr, plz)
            if self.userNameExists(username):
                return False, "username already exists"
            
            elif password != passwordConfirm:
              return False, "passwords do not match" 
            else:
                with self.connection:
                        cursor.execute(customer_query, parameters_customer)
                        return True, "customer added"

    def registerRestaurant(self, email, username, password,passwordConfirm, address, plz, restaurantname, description):
            cursor = self.connection.cursor()
            restaurant_query = "INSERT INTO restaurant(email, username, password, address, plz, restaurantname, description) VALUES (?, ?, ?, ?, ?, ?, ?)"
           
            parameters_restaurant = (email, username, password, address, plz, restaurantname, description)
            if self.userNameExists(username):
                return False, "username already exists"
            
            elif password != passwordConfirm:
              return False, "passwords do not match" 
            else:
                with self.connection:
                        cursor.execute(restaurant_query, parameters_restaurant)
                        return True, "restaurant added"
                    

