from table_operations.baseClass import baseClass
from tables import Eq_ramObj

class Eq_ram(baseClass):
    def __init__(self):
        super().__init__("EQ_RAM", Eq_ramObj)

    def add(self, eq_ram):
        query = "INSERT INTO EQ_RAM (RAM_TYPE, CAPACITY, FRE_SPEED, EQ_ID) VALUES (%s, %s, %s, %s) RETURNING EQ_ID"
        fill = (eq_ram.ram_type, eq_ram.capacity, eq_ram.fre_speed, eq_ram.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_RAM WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)