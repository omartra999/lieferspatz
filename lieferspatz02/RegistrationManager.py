import sqlite3
class registrationManager:
    
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def userNameExists(self, username):
        customer_query = "SELECT COUNT(*) FROM customer WHERE username = ?"        
        with self.connection:
            result = self.cursor.execute(customer_query, (username,)).fetchone()[0]
            return result > 0
        
    def restaurantExists(self, restaurant_name):
        restaurant_query = "SELECT COUNT(*) FROM restaurant WHERE restaurantname = ?"
        with self.connection:
            result = self.cursor.execute(restaurant_query, (restaurant_name,)).fetchone()[0]
            return result > 0



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
                return True, restaurant_id