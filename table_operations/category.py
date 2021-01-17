from table_operations.baseClass import baseClass
from tables import CategoryObj

class Category(baseClass):
    def __init__(self):
        super().__init__("CATEGORY", CategoryObj)

    def add(self, cat_name):
        query = "INSERT INTO CATEGORY (CAT_NAME) VALUES (%s)"
        fill = (cat_name)
        self.execute(query, fill)