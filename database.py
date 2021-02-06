from table_operations import address, category, comment, customer, person, customer_address,equipment, product, supplier, transaction, transaction_product, control
from table_operations.all_equipment import eq_case, eq_cooler, eq_headset, eq_keyboard, eq_monitor, eq_motherboard, eq_mouse, eq_powersupply, eq_processor, eq_ram, eq_videocard

class Database:
    def __init__(self):
        self.address = address.Address()
        self.category = category.Category()
        self.comment = comment.Comment()
        self.person = person.Person()
        self.customer = customer.Customer()
        self.customer_address = customer_address.CustomerAddress()
        self.equipment = equipment.Equipment()
        self.product = product.Product()
        self.supplier = supplier.Supplier()
        self.transaction = transaction.Transaction()
        self.transaction_product = transaction_product.TransactionProduct()
        self.control = control.Control()

        self.eq_case = eq_case.Eq_case()
        self.eq_cooler = eq_cooler.Eq_cooler()
        self.eq_headset = eq_headset.Eq_headset()
        self.eq_keyboard = eq_keyboard.Eq_keyboard()
        self.eq_monitor = eq_monitor.Eq_monitor()
        self.eq_motherboard = eq_motherboard.Eq_motherboard()
        self.eq_mouse = eq_mouse.Eq_mouse()
        self.eq_powersupply = eq_powersupply.Eq_powersupply()
        self.eq_processor = eq_processor.Eq_processor()
        self.eq_ram = eq_ram.Eq_ram()
        self.eq_videocard = eq_videocard.Eq_videocard()