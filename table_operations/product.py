import psycopg2 as dbapi2
from table_operations.baseClass import baseClass, url
from tables import ProductObj, EquipmentObj


class Product(baseClass):
    def __init__(self):
        super().__init__("PRODUCT", ProductObj)

    def add(self, product):
        query = "INSERT INTO PRODUCT (EQ_ID, REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        fill = (product.eq_id, product.remaining, product.price, product.number_of_sells, product.explanation, product.is_active)

        self.execute(query, fill)

        return product.eq_id

    def update(self, eq_id, product):
        query = "UPDATE PRODUCT SET REMAINING = %s, PRICE = %s, NUMBER_OF_SELLS = %s, EXPLANATION = %s, IS_ACTIVE = %s WHERE (EQ_ID = %s)"
        fill = (product.remaining, product.price, product.number_of_sells, product.explanation, product.is_active, eq_id)

        self.execute(query, fill)

        return eq_id

    def update_piece_and_remainig(self, eq_id, new_remaining, new_sold):
        query = "UPDATE PRODUCT SET REMAINING = %s, NUMBER_OF_SELLS = %s WHERE (EQ_ID = %s) "
        fill = (new_remaining, new_sold, eq_id)

        self.execute(query, fill)

        return eq_id

    def delete(self, eq_id):
        query = "DELETE FROM PRODUCT WHERE (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)

    def get_row(self, eq_id):
        _product = None

        query = "SELECT * FROM PRODUCT WHERE (EQ_ID = %s)"
        fill = (eq_id)

        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            product = cursor.fetchone()
            if product is not None:
                _product = ProductObj(product[0], product[1], product[2], product[3], product[4], product[5], product[6])

        return _product

    def get_table(self):
        products = []

        query = "SELECT * FROM PRODUCT;"

        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for product in cursor:
                product_ = ProductObj(product[0], product[1], product[2], product[3], product[4], product[5], product[6])
                products.append(product_)
            cursor.close()

        return products

    def get_products_all_info(self, eq_id=None, is_active=True):
        products_equipments = []

        query = "SELECT * FROM PRODUCT, EQUIPMENT " \
                "WHERE (PRODUCT.EQ_ID = EQUIPMENT.EQ_ID  " \
                "AND (PRODUCT.IS_ACTIVE = %s"
        fill = [is_active]

        if eq_id:
            query += " AND EQ_ID = %s"
            fill.append(eq_id)
        query += "))"

        fill = tuple(fill)

        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            for all_info in cursor:
                product_ = ProductObj(all_info[0], all_info[1], all_info[2], all_info[3], all_info[4], all_info[5], all_info[6])
                equipment_ = EquipmentObj(all_info[7], all_info[8], all_info[9], all_info[10], all_info[11])
                products_equipments.append([product_, equipment_])
            cursor.close()

        return products_equipments