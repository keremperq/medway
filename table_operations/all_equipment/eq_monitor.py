from table_operations.baseClass import baseClass
from tables import Eq_monitorObj

class Eq_monitor(baseClass):
    def __init__(self):
        super().__init__("EQ_MONITOR", Eq_monitorObj)

    def add(self, eq_monitor):
        query = "INSERT INTO EQ_MONITOR (SCREEN_SIZE, RESOLUTION, REFRESH_RATE, EQ_ID) VALUES (%s, %s, %s, %s)"
        fill = (eq_monitor.screen_size, eq_monitor.resolution, eq_monitor.refresh_rate, eq_monitor.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_MONITOR WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)