from table_operations.baseClass import baseClass
from tables import AddressObj

class Address(baseClass):
    def __init__(self):
        super().__init__("ADDRESS", AddressObj)

    def add(self, *values):
        '''
        @params address_name, country, city, neighborhood, street, address_no, zipcode, explanation
        '''
        assert len(values) == 8
        query = self.insertIntoFlex("ADDRESS_NAME", "COUNTRY", "CITY",  "NEIGHBORHOOD", "STREET", "ADDR_NUMBER", "ZIPCODE", "EXPLANATION")
        fill = (*values, )
        self.execute(query, fill)