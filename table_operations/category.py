from table_operations.baseClass import baseClass
from tables import CategoryObj

class Category(baseClass):
    def __init__(self):
        super().__init__("CATEGORY", CategoryObj)

    def add(self, category):
        query = "INSERT INTO CATEGORY (CAT_NAME) VALUES (%s) RETURNING CAT_ID"
        fill = (category.cat_name)
        self.execute(query, fill)