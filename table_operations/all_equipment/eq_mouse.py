from table_operations.baseClass import baseClass
from tables import Eq_mouseObj

class Eq_mouse(baseClass):
    def __init__(self):
        super().__init__("EQ_MOUSE", Eq_mouseObj)

    def add(self, eq_mouse):
        query = "INSERT INTO EQ_MOUSE (MOUSE_TYPE, DPI, BUTTONS, EQ_ID) VALUES (%s, %s, %s, %s)"
        fill = (eq_mouse.mouse_type, eq_mouse.dpi, eq_mouse.buttons, eq_mouse.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_MOUSE WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)