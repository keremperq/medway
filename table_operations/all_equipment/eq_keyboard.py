from table_operations.baseClass import baseClass
from tables import Eq_keyboardObj

class Eq_keyboard(baseClass):
    def __init__(self):
        super().__init__("EQ_KEYBOARD", Eq_keyboardObj)

    def add(self, eq_keyboard):
        query = "INSERT INTO EQ_KEYBOARD (KEYBOARD_TYPE, KEY_SEQUENCE, IS_MECHANIC, IS_RGB, EQ_ID) VALUES (%s, %s, %s, %s, %s) RETURNING EQ_ID"
        fill = (eq_keyboard.keyboard_type, eq_keyboard.key_sequence, eq_keyboard.is_mechanic, eq_keyboard.is_rgb, eq_keyboard.eq_id)
        self.execute(query, fill)

    def delete(self, eq_id):
        query = "DELETE FROM EQ_KEYBOARD WHERE  (EQ_ID = %s)"
        fill = (eq_id)
        self.execute(query, fill)