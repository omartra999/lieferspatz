import sqlite3
from PIL import Image
from io import BytesIO
import base64
from functions import f,default_logo_path,default_food_logo
from flask import Flask,request


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

    def add_item(self,item_name,detail,price,types,logo):
        try:
            with self.connection:
                query = "INSERT INTO menu(restaurant_id,item_name,detail,price,types) VALUES (? ,? ,?, ?, ?)"
                parameter =(self.id,item_name,detail,price,types)
                self.cursor.execute(query, parameter)
                menu_id = self.cursor.lastrowid#get the lastest menu id
                print("menu_id:",menu_id)
                self.set_default_food_logo(menu_id)
                if (logo != None):
                    self.updated_food_logo(menu_id,logo) 
                return True, "item is added"
        except Exception as e:
            print(f"an Error accured: {e}")

    def get_item(self, item_id):
        try:
            with self.connection:
                query = "SELECT item_name, detail, price, types FROM menu WHERE restaurant_id = ? AND id = ?"
                item = self.cursor.execute(query, (self.id, item_id)).fetchall()
                return item
        except Exception as e:
            print(f"an error occured: {e}")
            return False

    def getFood(self):
        try:
            with self.connection:
                query = "SELECT item_name, detail, price, types FROM menu WHERE restaurant_id = ? AND types = food"
                food = self.cursor.execute(query, (self.id,)).fetchall()
                return food
        except Exception as e:
            print(f"an error accured : {e}")
            return False

    def getDrinks(self):
        try:
            with self.connection:
                query = "SELECT item_name, detail, price, types FROM menu WHERE restaurant_id = ? AND types = drink"
                drinks = self.cursor.execute(query, (self.id,)).fetchall()
                return drinks
        except Exception as e:
            print(f"an error accured : {e}")
            return False
    def getMenu(self):
        try:
            with self.connection:
                query = "SELECT id ,item_name, detail, price, types FROM menu WHERE restaurant_id = ?"
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
    
    def delete_item(self, item_id):
        try:
            with self.connection:
                query = "DELETE FROM menu WHERE restaurant_id = ? AND id = ?"
                self.cursor.execute(query, (self.id, item_id,))
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
                 query = "SELECT * FROM Orders WHERE restaurant_id =  ? AND STATUS = 'open'" 
                 orders = self.cursor.execute(query, (self.id,)).fetchall()
                 return (orders)
        except Exception as e:
            print(f"an error accured: {e}")
            return False

    def get_accepted_orders(self):
        try:
            with self.connection:
                query = "SELECT * FROM Orders WHERE restaurant_id =  ? AND (STATUS = 'accepted' OR STATUS = 'preparing')"
                orders = self.cursor.execute(query, (self.id,)).fetchall()
                return (orders)
        except Exception as e:
            print(f"an error accured: {e}")
            return False

    def update_order_status(self, order_id, status):
        try:
            with self.connection:
                query = "UPDATE Orders SET status = ? WHERE restaurant_id = ? AND id = ? "
                self.cursor.execute(query,(status,self.id,order_id,))
            self.connection.commit()
            return True
        except Exception as e: 
            print(f"an error accured: {e}")
    
    def get_order_history(self):
        try:
            with self.connection:
                query = "SELECT * FROM Orders WHERE restaurant_id = ? "
                orders = self.cursor.execute(query, (self.id,)).fetchall()
                return orders
        except Exception as e:
            print(f"an error accured: {e}")
            return False

    def clear_history(self):
        try:
            with self.connection:
                query = "DELETE FROM Orders WHERE restaurant_id = ? AND STATUS ='delivered' "
                self.cursor.execute(query,(self.id,))
            self.connection.commit()
            return True
        except Exception as e: 
            print(f"an error accured: {e}") 
    @staticmethod    
    def convertToBinaryData(filename):
        #just so that i don't forget, this accepts the binary data  from the FileStorage object
        blobData=filename.read()
        #print("readed: ", blobData)
        return blobData
    
    def updateRestaurantImage(self, logo_file):
        try:
            with self.connection:
                query = "UPDATE restaurant_logo SET logo = :logo WHERE restaurant_id = :id"
                new_image_data = self.convertToBinaryData(logo_file)

                if new_image_data:
                    #print("New Image Data:", new_image_data)  # Add this line

                    new_image = Image.open(BytesIO(new_image_data))
                    buffered = BytesIO()
                    new_image.save(buffered, format="PNG")
                    new_blob_data = buffered.getvalue()
                    data_dict = {'logo': new_blob_data, 'id': self.id}
                    self.connection.cursor().execute(query, data_dict)

                    print("Updated Image Data:", len(new_blob_data))  # Add this line

                    return True
                else:
                    return False

        except sqlite3.Error as error:
            print("Failed to update restaurant image in SQLite table:", error)
            return False
        finally:
            self.connection.commit()

    
    def getLogo(self):
        try:
            with self.connection:
                query = "SELECT * FROM restaurant_logo WHERE restaurant_id = ?"
                result = self.cursor.execute(query, (self.id,)).fetchone()
                if result:
                    logo_data = result[2]
                    if logo_data:
                    # Convert the binary data to base64-encoded string
                        logo_base64 = base64.b64encode(logo_data).decode('utf-8')
                        return logo_base64

                else:
                    return None
        except sqlite3.Error as error:
            print("Failed to retrieve restaurant logo from SQLite table", error)
            return None
        
    def set_default_food_logo(self,menu_id):
        logo_query = "INSERT INTO food_logo(restaurant_id,menu_id, logo) VALUES (?, ?, ?)"
        with open(default_food_logo, 'rb') as default_logo_file:
            default_logo_data = default_logo_file.read()

        parameters_logo = (self.id, menu_id, default_logo_data)

        with self.connection:
            self.cursor.execute(logo_query, parameters_logo)

    def updated_food_logo(self,menu_id,logo_file):
        try:
            with self.connection:
                query = "UPDATE food_logo SET logo = :logo WHERE (restaurant_id = :id AND menu_id = :menu_id)"
                new_image_data = self.convertToBinaryData(logo_file)

                if new_image_data:
                    #print("New Image Data:", new_image_data)  # Add this line

                    new_image = Image.open(BytesIO(new_image_data))
                    buffered = BytesIO()
                    new_image.save(buffered, format="PNG")
                    new_blob_data = buffered.getvalue()
                    data_dict = {'logo': new_blob_data, 'id': self.id,'menu_id': menu_id}
                    self.connection.cursor().execute(query, data_dict)

                    print("Updated Image Data:", len(new_blob_data))  # Add this line

                    return True
                else:
                    return False

        except sqlite3.Error as error:
            print("Failed to update restaurant image in SQLite table:", error)
            return False
        finally:
            self.connection.commit()
    
    def getfoodLogo(self,menu_id):
        try:
            with self.connection:
                query = "SELECT * FROM food_logo WHERE (restaurant_id = ? AND menu_id = ?)"
                result = self.cursor.execute(query, (self.id,menu_id,)).fetchone()
                if result:
                    logo_data = result[3]
                    if logo_data:
                    # Convert the binary data to base64-encoded string
                        logo_base64 = base64.b64encode(logo_data).decode('utf-8')
                        return logo_base64

                else:
                    return None
        except sqlite3.Error as error:
            print("Failed to retrieve restaurant logo from SQLite table", error)
            return None