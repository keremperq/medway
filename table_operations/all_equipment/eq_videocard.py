from table_operations.baseClass import baseClass
from tables import Eq_videocardObj

class Eq_videocard(baseClass):
    def __init__(self):
        super().__init__("EQ_VIDEOCARD", Eq_videocardObj)

    def add(self, eq_videocard):
        query = "INSERT INTO EQ_VIDEOCARD (MEMORY_SIZE, CORE_SPEED, GPU_MODEL, MANUFACTURER, EQ_ID) VALUES (%s, %s, %s, %s, %s)"
        fill = (eq_videocard.memory_size, eq_videocard.core_speed, eq_videocard.gpu_model, eq_videocard.manufacturer, eq_videocard.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_VIDEOCARD WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)