from table_operations.baseClass import baseClass
from tables import CustomerObj

class Customer(baseClass):
    def __init__(self):
        super().__init__("CUSTOMER", CustomerObj)

    def add(self, *values):
        '''
        @param customer_name, surname, username, is_active, email, phone, password, address_id
        '''
        assert len(values) == 6
        query = self.insertIntoFlex("CUSTOMER_NAME", "SURNAME", "USERNAME", "IS_ACTIVE", "EMAIL", "PHONE", "PASSWORD", "ADDRESS_ID") + " RETURNING CUSTOMER_ID"
        fill = (*values, )
        last_customer_id = (self.execute(query, fill, True))[0][0]
        return last_customer_id if last_customer_id is not None else -1