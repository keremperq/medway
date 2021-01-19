from table_operations.baseClass import baseClass
from tables import Eq_coolerObj

class Eq_cooler(baseClass):
    def __init__(self):
        super().__init__("EQ_COOLER", Eq_coolerObj)

    def add(self, eq_cooler):
        query = "INSERT INTO EQ_COOLER (COOLER_TYPE, COOLER_SIZE, LED_COLOR, EQ_ID) VALUES (%s, %s, %s, %s) RETURNING EQ_ID"
        fill = (eq_cooler.cooler_type, eq_cooler.cooler_size, eq_cooler.led_color, eq_cooler.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_COOLER WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)