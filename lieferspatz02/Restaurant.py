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
                menu = self.cursor.execute(query,(self.id,)).fetchall()
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
        
    def plz_exists(self, plz):
        try:
            with self.connection:
                query = "SELECT COUNT(*) FROM postal WHERE restaurant_id = ? AND plz = ?"
                result = self.cursor.execute(query, (self.id, plz)).fetchone()[0]
                return result > 0
        except Exception as e:
            print(f"an error accured: {e}")
            return False

    def add_plz(self, plz_list):
        try:
            with self.connection:
                query = "INSERT INTO postal(restaurant_id, plz) VALUES (?, ?)"
                for plz in plz_list:
                    print("list: ", plz_list)
                    if self.plz_exists(plz) == False:
                        self.cursor.execute(query, (self.id, plz,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"an error accured: {e}")
            return False
        
    def delete_plz(self, plz):
        try: 
            with self.connection:
                for area in plz:
                    query = "DELETE FROM postal WHERE restaurant_id = ? AND plz = ?"
                    self.cursor.execute(query, (self.id, area,))
                print("Deleted rows:", self.cursor.rowcount)
            self.connection.commit()
            return True
        except Exception as e: 
            print(f"an error accured: {e}")
            return False
    
    def get_delivery_raduis(self):
        try:
            with self.connection:
                query = "SELECT plz FROM postal WHERE restaurant_id = ?"
                delivers = self.cursor.execute(query, (self.id,)).fetchall()
            return delivers
        except Exception as e:
            print(f"an error accured: {e}")
            return False
    
    def delivers(self, plz):
        try: 
            with self.connection:
                query = "SELECT COUNT(*) FROM postal WHERE restaurant_id = ? AND plz = ?"
                result = self.cursor.execute(query,(self.id, plz,)).fetchone()[0]
                return result > 0
        except Exception as e:
            print(f"an error accured: {e}")
            return False
        
    def get_open_orders(self):
        try:
            with self.connection:
                query = "SELECT customer_id, item_id FROM orders WHERE restaurant_id = ?, status = open "
                orders = self.cursor.execute(query, (self.id,)).fetchall()
                return(orders)
        except Exception as e:
            print(f"an error accured: {e}")
            return False

    def update_order_status(self, order_id, status):
        try:
            with self.connection:
                query = "UPDATE orders SET status = ? WHERE restaurant_id = ? AND id = ? "
                self.cursor.execute(query,(status,self.id,order_id,))
            self.connection.commit()
            return True
        except Exception as e: 
            print(f"an error accured: {e}")
    
    def get_order_history(self):
        try:
            with self.connection:
                query = "SELECT id, customer_id, status FROM orders WHERE restaurant_id = ?"
                orders = self.cursor.execute(query, (self.id))
                return orders
        except Exception as e:
            print(f"an error accured: {e}")
            return False
        
class logo:
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)

    @staticmethod
    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def updateRestaurantImage(self,id,logo):
        try:
            with self.connection:

                query = "UPDATE restaurant SET logo = ? WHERE id = ?"

                newImage = self.convertToBinaryData(logo)

                data_tuple = (newImage, id)

                self.connection.cursor().execute(query, data_tuple)
                self.connection.commit()
                return True

        except sqlite3.Error as error:
            print("Failed to update restaurant image in SQLite table", error)
            return False
        finally:
            if self.connection:
                self.connection.close()