from table_operations.baseClass import baseClass
from tables import PersonObj

class Person(baseClass):
    def __init__(self):
        super().__init__("PERSON", PersonObj)

    def add(self, *values):
        '''
        @param person_name, person_surname
        '''
        assert len(values) == 2
        query = self.insertIntoFlex("PERSON_NAME", "SURNAME") + " RETURNING PERSON_ID"
        fill = (*values, )
        last_person_id = (self.execute(query, fill, True))[0][0]
        return last_person_id if last_person_id is not None else -1