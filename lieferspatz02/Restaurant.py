import sqlite3

class _restaurant:
    def __init__(self, id, connection):
        self.id = id
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def userNameExists(self, username):
        query = "SELECT COUNT(*) FROM restaurant WHERE username = ?"
        try:
            with self.connection:
                result = self.cursor.execute(query,(username,)).fetchone()[0]
                return result > 0
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False




    def get_username(self):
        query = "SELECT username FROM restaurant WHERE id = ?"
        try:
            with self.connection:
                username = self.cursor.execute(query, (self.id,)).fetchone()[0]
                return username
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False

    def get_address(self):
        query = "SELECT address FROM restaurant WHERE id = ?"
        try:
            with self.connection:
                address = self.cursor.execute(query, (self.id,)).fetchone()[0]
                return address
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False


    def get_email(self):
        query = "SELECT email FROM restaurant WHERE id = ?"
        try:
            with self.connection:
                email = self.cursor.execute(query, (self.id,)).fetchone()[0]
                return email
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False

    
    def get_plz(self):
        query = "SELECT plz FROM restaurant WHERE id = ?"
        try:
            with self.connection:
                plz = self.cursor.execute(query, (self.id,)).fetchone()[0]
                return plz
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False


    def get_restaurant_name(self):
        query = "SELECT restaurantname FROM restaurant WHERE id = ?"
        try:
            with self.connection:
                name = self.cursor.execute(query, (self.id,)).fetchone()[0]
                return name
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False

    def get_description(self):
        query = "SELECT description FROM restaurant WHERE id = ?"
        try:
            with self.connection:
                description = self.cursor.execute(query, (self.id,)).fetchone()[0]
                return description
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False


    
    def set_username(self, username):
        query = "UPDATE restaurant SET username = ? WHERE id = ?"
        if not self.userNameExists(username):
            try:
                with self.connection:
                    self.cursor.execute(query, (username, self.id,))
                    self.connection.commit()
                    return True
            except Exception as e:
              print(f"An Error occurred: {e}")
              return False

        else:
            return "Username already exists"

    def set_address(self, address):
        query = "UPDATE restaurant SET address = ? WHERE id = ?"
        try:
            with self.connection:
                self.cursor.execute(query, (address, self.id,))
                self.connection.commit()
                return True
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False

    def set_email(self, email):
        query = "UPDATE restaurant SET email = ? WHERE id = ?"
        try:
            with self.connection:
                self.cursor.execute(query, (email, self.id,))
                self.connection.commit()
                return True
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False

    def set_plz(self, plz):
        query = "UPDATE restaurant SET plz = ? WHERE id = ?"
        try:
            with self.connection:
                self.cursor.execute(query, (plz, self.id,))
                self.connection.commit()
                return True
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False


    def set_restaurant_name(self, name):
        query = "UPDATE restaurant SET restaurantname = ? WHERE id = ?"
        try:
            with self.connection:
                self.cursor.execute(query, (name, self.id,))
                self.connection.commit()
                return True
        except Exception as e:
            print(f"An Error occurred: {e}")
            return False

    def set_description(self, description):
        query = "UPDATE restaurant SET description = ? WHERE id = ?"
        try:
            with self.connection:
                self.cursor.execute(query, (description, self.id))
                self.connection.commit()
                return True
        except Exception as e:
            return f"an error accured: {e}"
        
            ## check for replicated item name
    def item_exist(self, restaurant_id ,item_name):
        try:
            with self.connection:
                query = "SELECT COUNT(*) FROM menu WHERE restaurant_id = ? AND item_name = ?" 
                result = self.cursor.execute(query, (restaurant_id ,item_name,)).fetchone()[0]
                return result > 0
        except Exception as e:
            print(f"an error accured: {e}")
            return False
        
    ## create item into menu
    def add_item(self,item_name,detail,price,type):
        try:
            with self.connection:
                query = "INSERT INTO menu(restaurant_id,item_name,detail,price,type) VALUES (? ,? ,?, ?, ?)"
                parameter =(self.id,item_name,detail,price,type)
                self.cursor.execute(query, parameter)
                return True, "item is added"
        except Exception as e:
            print(f"an Error accured: {e}")

    def getFood(self):
        try:
            with self.connection:
                query = "SELECT item_name, detail, price, type FROM menu WHERE restaurant_id = ? AND type = food"
                food = self.cursor.execute(query, (self.id,)).fetchall()
                return food
        except Exception as e:
            print(f"an error accured : {e}")
            return False

    def getDrinks(self):
        try:
            with self.connection:
                query = "SELECT item_name, detail, price, type FROM menu WHERE restaurant_id = ? AND type = drink"
                drinks = self.cursor.execute(query, (self.id,)).fetchall()
                return drinks
        except Exception as e:
            print(f"an error accured : {e}")
            return False
    def getMenu(self):
        try:
            with self.connection:
                query = "SELECT item_name, detail, price, type FROM menu WHERE restaurant_id = ?"
                menu = self.cursor.execute(query,(self.id,))
                return menu
        except Exception as e:
            print(f"an error accured: {e}")
            return False
    
    def emptyMenu(self):
        try:
            with self.connection:
                query = "DELETE FROM menu WHERE id = ?"
                self.cursor.execute(query, (self.id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"an error accured: {e}")
            return False
    
    def delete_item(self, item_name):
        try:
            with self.connection:
                query = "DELETE FROM menu WHERE restaurant_id = ? AND item_name = ?"
                self.cursor.execute(query, (self.id, item_name,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"an error accured: {e}")
            return False