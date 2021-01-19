from table_operations.baseClass import baseClass
from tables import Eq_powersupplyObj

class Eq_powersupply(baseClass):
    def __init__(self):
        super().__init__("EQ_POWERSUPPLY", Eq_powersupplyObj)

    def add(self, eq_powersupply):
        query = "INSERT INTO EQ_POWERSUPPLY (POWER_W, POWER_TYPE, SATA_CONNECTION, EQ_ID) VALUES (%s, %s, %s, %s) RETURNING EQ_ID"
        fill = (eq_powersupply.power_w, eq_powersupply.power_type, eq_powersupply.sata_connection, eq_powersupply.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_POWERSUPPLY WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)