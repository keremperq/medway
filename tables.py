from flask_login import UserMixin

class EquipmentObj:
    def __init__(self, eq_id, eq_name, eq_brand, eq_image, cat_id):
        self.eq_id = eq_id
        self.eq_name = eq_name
        self.eq_brand = eq_brand
        self.eq_image = eq_image
        self.cat_id = cat_id


class AddressObj:
    def __init__(self, address_id, address_name, country, city, neighborhood, street, address_no, zipcode, explanation):
        self.address_id = address_id
        self.address_name = address_name
        self.country = country
        self.city = city
        self.neighborhood = neighborhood
        self.street = street
        self.address_no = address_no
        self.zipcode = zipcode
        self.explanation = explanation


class CategoryObj:
    def __init__(self, cat_id, cat_name):
        self.cat_id = cat_id
        self.cat_name = cat_name


class CommentObj:
    def __init__(self, customer_id, eq_id, comment_title, comment_statement, added_time=None, updated_time=None, comment_id=None):
        self.comment_id = comment_id
        self.customer_id = customer_id
        self.eq_id = eq_id
        self.comment_title = comment_title
        self.comment_statement = comment_statement
        self.added_time = added_time
        self.updated_time = updated_time


class CustomerObj(UserMixin):
    def __init__(self, customer_id, customer_name,surname, username, email, password, phone, address_id,is_active=True):
        self.id = customer_id
        self.customer_name = customer_name
        self.surname = surname
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.address_id = address_id
        self.is_active = is_active
        self.is_admin = self.id == 1     # To make user with customer_id = 1 admin


class ProductObj:
    def __init__(self, eq_id, remaining, price, number_of_sells, explanation, is_active, supp_id):
        self.eq_id = eq_id
        self.remaining = remaining
        self.price = price
        self.number_of_sells = number_of_sells
        self.explanation = explanation
        self.is_active = is_active
        self.supp_id = supp_id


class SupplierObj:
    def __init__(self, supp_id, supplier_name, phone, supp_address):
        self.supp_id = supp_id
        self.supplier_name = supplier_name
        self.phone = phone
        self.supp_address = supp_address


class TransactionObj:
    def __init__(self, transaction_id, customer_id, address_id, transaction_time, payment_type, transaction_explanation, is_completed):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.address_id = address_id
        self.transaction_time = transaction_time
        self.payment_type = payment_type
        self.transaction_explanation = transaction_explanation
        self.is_completed = is_completed


class TransactionProductObj:
    def __init__(self, transaction_id, eq_id, piece, discount, unit_price):
        self.transaction_id = transaction_id
        self.eq_id = eq_id
        self.piece = piece
        self.discount = discount
        self.unit_price = unit_price


class Eq_caseObj:
    def __init__(self, eq_id, case_type, has_audio, is_transparent, has_psu):
        self.eq_id = eq_id
        self.case_type = case_type
        self.has_audio = has_audio
        self.is_transparent = is_transparent
        self.has_psu = has_psu


class Eq_coolerObj:
    def __init__(self, eq_id, cooler_type, cooler_size, led_color):
        self.eq_id = eq_id
        self.cooler_type = cooler_type
        self.cooler_size = cooler_size
        self.led_color = led_color

class Eq_headsetObj:
    def __init__(self, eq_id, usage_area, headset_type, has_mic):
        self.eq_id = eq_id
        self.usage_area = usage_area
        self.headset_type = headset_type
        self.has_mic = has_mic

class Eq_keyboardObj:
    def __init__(self, eq_id, keyboard_type, key_sequence, is_mechanic, is_rgb):
        self.eq_id = eq_id
        self.keyboard_type = keyboard_type
        self.key_sequence = key_sequence
        self.is_mechanic = is_mechanic
        self.is_rgb = is_rgb

class Eq_monitorObj:
    def __init__(self, eq_id, screen_size, resolution, refresh_rate):
        self.eq_id = eq_id
        self.screen_size = screen_size
        self.resolution = resolution
        self.refresh_rate = refresh_rate


class Eq_motherboardObj:
    def __init__(self, eq_id, ram_type, max_ram, ram_slot_number, socket_type, ram_fre_speed):
        self.eq_id = eq_id
        self.ram_type = ram_type
        self.max_ram = max_ram
        self.ram_slot_number = ram_slot_number
        self.socket_type = socket_type
        self.ram_fre_speed = ram_fre_speed

class Eq_mouseObj:
    def __init__(self,eq_id, mouse_type,dpi,buttons):
        self.eq_id = eq_id
        self.mouse_type = mouse_type
        self.dpi = dpi
        self.buttons = buttons

class Eq_powersupplyObj:
    def __init__(self,eq_id,power_w,power_type,sata_connection):
        self.eq_id = eq_id
        self.power_w = power_w
        self.power_type = power_type
        self.sata_connection = sata_connection

class Eq_processorObj:
    def __init__(self,eq_id,model,fre_speed,core_number):
        self.eq_id = eq_id
        self.model = model
        self.fre_speed = fre_speed
        self.core_number = core_number

class Eq_ramObj:
    def __init__(self,eq_id,ram_type,capacity,fre_speed):
        self.eq_id = eq_id
        self.ram_type = ram_type
        self.capacity = capacity
        self.fre_speed = fre_speed

class Eq_videocardObj:
    def __init__(self, eq_id, memory_size, core_speed, gpu_model,manufacturer):
        self.eq_id = eq_id
        self.memory_size = memory_size
        self.core_speed = core_speed
        self.gpu_model = gpu_model
        self.manufacturer = manufacturer

