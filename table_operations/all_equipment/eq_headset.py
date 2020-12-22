from table_operations.baseClass import baseClass
from tables import Eq_headsetObj

class Eq_headset(baseClass):
    def __init__(self):
        super().__init__("EQ_HEADSET", Eq_headsetObj)

    def add(self, eq_headset):
        query = "INSERT INTO EQ_HEADSET (USAGE_AREA, HEADSET_TYPE, HAS_MIC, EQ_ID) VALUES (%s, %s, %s, %s)"
        fill = (eq_headset.usage_area, eq_headset.headset_type, eq_headset.has_mic, eq_headset.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_HEADSET WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)