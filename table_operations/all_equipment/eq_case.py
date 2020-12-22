from table_operations.baseClass import baseClass
from tables import Eq_caseObj

class Eq_case(baseClass):
    def __init__(self):
        super().__init__("EQ_CASE", Eq_caseObj)

    def add(self, eq_case):
        query = "INSERT INTO EQ_CASE (CASE_TYPE, HAS_AUDIO, IS_TRANSPARENT, HAS_PSU, EQ_ID) VALUES (%s, %s, %s, %s, %s)"
        fill = (eq_case.case_type, eq_case.has_auido, eq_case.is_transparent, eq_case.has_psu, eq_case.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_CASE WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)

