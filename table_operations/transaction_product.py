import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import TransactionProductObj


class TransactionProduct(baseClass):
    def __init__(self):
        super().__init__("TRANSACTION_PRODUCT", TransactionProductObj)

    def add(self, transaction_product):
        query = "INSERT INTO TRANSACTION_PRODUCT (TRANSACTION_ID, PIECE, DISCOUNT, UNIT_PRICE, EQ_ID) VALUES (%s, %s, %s, %s, %s)"
        fill = (transaction_product.transaction_id, transaction_product.piece, transaction_product.discount, transaction_product.unit_price, transaction_product.eq_id)
        self.execute(query, fill)

    def delete(self, transaction_id, eq_id):
        query = "DELETE FROM TRANSACTION_PRODUCT WHERE ((TRANSACTION_ID = %s) AND (EQ_ID = %s))"
        fill = (transaction_id, eq_id)
        self.execute(query, fill)