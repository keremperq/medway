from table_operations.baseClass import baseClass
from tables import Eq_motherboardObj

class Eq_motherboard(baseClass):
    def __init__(self):
        super().__init__("EQ_MOTHERBOARD", Eq_motherboardObj)

    def add(self, eq_motherboard):
        query = "INSERT INTO EQ_MOTHERBOARD (RAM_TYPE, MAX_RAM, RAM_SLOT_NUMBER, SOCKET_TYPE, RAM_FRE_SPEED, EQ_ID) VALUES (%s, %s, %s, %s, %s, %s)"
        fill = (eq_motherboard.ram_type, eq_motherboard.max_ram, eq_motherboard.ram_slot_number, eq_motherboard.socket_type, eq_motherboard.ram_fre_speed, eq_motherboard.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_MOTHERBOARD WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)