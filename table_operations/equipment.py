import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import EquipmentObj

class Equipment(baseClass):
    def __init__(self):
        super().__init__("EQUIPMENT", EquipmentObj)

    def add_equipment(self, equipment):
        query = "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES (%s, %s, %s, %s) RETURNING EQ_ID"
        fill = (equipment.eq_name , equipment.eq_brand, equipment.eq_image, equipment.cat_id)

        last_eq_id = (self.execute(query, fill, True))[0][0]

        return last_eq_id if last_eq_id is not None else -1

    def update(self, eq_key, equipment):
        query = "UPDATE EQUIPMENT SET EQ_NAME = %s, EQ_BRAND = %s, EQ_IMAGE = %s, CAT_ID = %s WHERE EQ_ID = %s"
        fill = (equipment.eq_name, equipment.eq_brand, equipment.eq_image,equipment.cat_id, eq_key)
        self.execute(query, fill)

        return eq_key

    def delete(self, eq_key):
        query1 = "DELETE FROM CATEGORY WHERE EQ_ID = %s"
        query2 = "DELETE FROM EQUIPMENT WHERE EQ_ID = %s"
        fill = (eq_key, )
        self.execute(query1, fill)
        self.execute(query2, fill)

    def get_row(self, eq_key):
        return super().get_row("*", ["EQ_ID"], [eq_key])

