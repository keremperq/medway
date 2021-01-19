from table_operations.baseClass import baseClass
from tables import Eq_processorObj

class Eq_processor(baseClass):
    def __init__(self):
        super().__init__("EQ_PROCESSOR", Eq_processorObj)

    def add(self, eq_processor):
        query = "INSERT INTO EQ_PROCESSOR (MODEL, FRE_SPEED, CORE_NUMBER, EQ_ID) VALUES (%s, %s, %s, %s) RETURNING EQ_ID"
        fill = (eq_processor.model, eq_processor.fre_speed, eq_processor.core_number, eq_processor.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_PROCESSOR WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)