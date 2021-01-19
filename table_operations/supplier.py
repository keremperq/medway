import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import SupplierObj

class Supplier(baseClass):
    def __init__(self):
        super().__init__("SUPPLIER", SupplierObj)

    def add(self, supplier):
        query = "INSERT INTO SUPPLIER (SUPPLIER_NAME, SUPP_PHONE, SUPP_ADDRESS) VALUES (%s, %s, %s) RETURNING SUPP_ID"
        fill = (supplier.supplier_name, supplier.supp_phone, supplier.supp_address)
        self.execute(query, fill)

    def delete(self, supp_id):
        query = "DELETE FROM SUPPLIER WHERE (SUPP_ID = %s)"
        fill = (supp_id)
        self.execute(query, fill)    