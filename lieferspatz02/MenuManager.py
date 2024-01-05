import sqlite3

class menuManager:
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
    
    ## check for replicated item name
    def item_exist(self,item_name):
        with self.connection:
            query = "SELECT COUNT(*) FROM menu WHERE item_name = ?" 
            result = self.connection.cursor().execute(query, (item_name,)).fetchone()[0]
            return result > 0
        
    ## create item into menu
    def create_item(self,restaurant,item_name,detail,price):
        with self.connection:
            query = "INSERT INTO menu(restaurant,item_name,detail,price) VALUES (? ,? ,?, ?)"
            parameter =(restaurant,item_name,detail,price)
            if self.item_exist(item_name):
                return False, "Item name exists, please change."
            else:
                with self.connection:
                    self.connection.cursor().execute(query, parameter)
                    return True, "item is added"