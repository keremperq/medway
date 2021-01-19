from flask import Flask, abort, render_template
from flask_login import LoginManager
from database import Database
from views import *

lm = LoginManager()
db = Database()

@lm.user_loader
def load_user(user_id):
    return db.customer.get_row("*", "CUSTOMER_ID", user_id)


@lm.unauthorized_handler
def unauthorized_access():
    return abort(401)

def create_app():

    app2 = Flask(__name__)
    app2.config.from_object("settings")
    app2.config["db"] = db

    lm.init_app(app2)
    lm.login_view = login_view.login_page

    app2.add_url_rule("/", view_func=general_views.home_page)
    app2.add_url_rule("/login", view_func=login_view.login_page, methods=["GET", "POST"])
    app2.add_url_rule("/logout", view_func=login_view.logout_page)
    app2.add_url_rule("/signup", view_func=login_view.signup_page, methods=["GET", "POST"])

    # Equipment pages
    app2.add_url_rule("/equipments", view_func=equipment_view.equipments_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/add-new", view_func=equipment_view.equipment_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:equipment_key>", view_func=equipment_view.equipment_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:equipment_key>/edit", view_func=equipment_view.equipment_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:equipment_key>/delete", view_func=equipment_view.equipment_delete_page)

    # Eq_case pages
    app2.add_url_rule("/equipments/add-eq-case", view_func=eq_case_view.eq_case_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_case_view.eq_case_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_case_view.eq_case_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_case_view.eq_case_delete_page, methods=["GET", "POST"])

    # Eq_cooler pages
    app2.add_url_rule("/equipments/add-eq-cooler", view_func=eq_cooler_view.eq_cooler_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_cooler_view.eq_cooler_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_cooler_view.eq_cooler_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_cooler_view.eq_cooler_delete_page, methods=["GET", "POST"])

    # Eq_headset pages
    app2.add_url_rule("/equipments/add-eq-headset", view_func=eq_headset_view.eq_headset_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_headset_view.eq_headset_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_headset_view.eq_headset_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_headset_view.eq_headset_delete_page, methods=["GET", "POST"])

    # Eq_keyboard pages
    app2.add_url_rule("/equipments/add-eq-keyboard", view_func=eq_keyboard_view.eq_keyboard_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_keyboard_view.eq_keyboard_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_keyboard_view.eq_keyboard_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_keyboard_view.eq_keyboard_delete_page, methods=["GET", "POST"])

    # Eq_monitor pages
    app2.add_url_rule("/equipments/add-eq-monitor", view_func=eq_monitor_view.eq_monitor_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_monitor_view.eq_monitor_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_monitor_view.eq_monitor_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_monitor_view.eq_monitor_delete_page, methods=["GET", "POST"])

    # Eq_motherboard pages
    app2.add_url_rule("/equipments/add-eq-motherboard", view_func=eq_motherboard_view.eq_motherboard_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_motherboard_view.eq_motherboard_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_motherboard_view.eq_motherboard_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_motherboard_view.eq_motherboard_delete_page, methods=["GET", "POST"])

    # Eq_mouse pages
    app2.add_url_rule("/equipments/add-eq-mouse", view_func=eq_mouse_view.eq_mouse_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_mouse_view.eq_mouse_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_mouse_view.eq_mouse_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_mouse_view.eq_mouse_delete_page, methods=["GET", "POST"])

    # Eq_powersupply pages
    app2.add_url_rule("/equipments/add-eq-powersupply", view_func=eq_powersupply_view.eq_powersupply_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_powersupply_view.eq_powersupply_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_powersupply_view.eq_powersupply_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_powersupply_view.eq_powersupply_delete_page, methods=["GET", "POST"])

    # Eq_processor pages
    app2.add_url_rule("/equipments/add-eq-processor", view_func=eq_processor_view.eq_processor_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_processor_view.eq_processor_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_processor_view.eq_processor_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_processor_view.eq_processor_delete_page, methods=["GET", "POST"])

    # Eq_ram pages
    app2.add_url_rule("/equipments/add-eq-ram", view_func=eq_ram_view.eq_ram_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_ram_view.eq_ram_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_ram_view.eq_ram_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_ram_view.eq_ram_delete_page, methods=["GET", "POST"])

    # Eq_videocard pages
    app2.add_url_rule("/equipments/add-eq-videocard", view_func=eq_videocard_view.eq_videocard_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>", view_func=eq_videocard_view.eq_videocard_page)
    app2.add_url_rule("/equipments/<int:eq_id>/edit", view_func=eq_videocard_view.eq_videocard_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/equipments/<int:eq_id>/delete", view_func=eq_videocard_view.eq_videocard_delete_page, methods=["GET", "POST"])

    # Product pages
    app2.add_url_rule("/products", view_func=product_view.products_page, methods=["GET", "POST"])
    app2.add_url_rule("/products/add-new", view_func=product_view.product_add_page, methods=["GET", "POST"])
    app2.add_url_rule("/products/<int:eq_id>", view_func=product_view.product_page, methods=["GET", "POST"])
    app2.add_url_rule("/products/<int:eq_id>/edit", view_func=product_view.product_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/products/<int:eq_id>/delete", view_func=product_view.product_delete_page, methods=["GET", "POST"])

    # Comment pages
    app2.add_url_rule("/comments", view_func=comment_view.comments_page)
    app2.add_url_rule("/comments/<int:comment_id>/edit", view_func=comment_view.comment_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/comments/<int:comment_id>/delete", view_func=comment_view.comment_delete_page)

    # Transaction (Shopping Cart)
    app2.add_url_rule("/shopping-cart", view_func=transaction_view.transaction_page)
    app2.add_url_rule("/shopping-cart/next", view_func=transaction_view.transaction_next_page, methods=["GET", "POST"])
    app2.add_url_rule("/shopping-cart/tp-<int:transaction_id>-<int:eq_id>/delete", view_func=transaction_view.tp_delete_page)

    # Address
    app2.add_url_rule("/addresses", view_func=address_view.addresses_page)
    app2.add_url_rule("/addresses/add-new", view_func=address_view.add_address, methods=["GET", "POST"])
    app2.add_url_rule("/addresses/<int:address_id>/edit", view_func=address_view.address_edit_page, methods=["GET", "POST"])
    app2.add_url_rule("/addresses/<int:address_id>/delete", view_func=address_view.address_delete_page, methods=["GET", "POST"])

    # Category
    app2.add_url_rule("/categories", view_func=category_view.categories_page)
    app2.add_url_rule("/categories/<int:cat_id>/equipments", view_func=category_view.equipments_by_category_page, methods=["GET", "POST"])

    # Customer
    app2.add_url_rule("/customers", view_func=customer_view.customers_page)
    app2.add_url_rule("/customers/<int:customer_id>/edit", view_func=customer_view.edit_customer_page, methods=["GET", "POST"])
    app2.add_url_rule("/customers/<int:customer_id>/delete", view_func=customer_view.delete_customer_page)

    return app2


app = create_app()

@app.errorhandler(401)
def unauthorized_access_page(err):
    return render_template("error/401.html")

@app.errorhandler(403)
def access_denied_page(err):
    return render_template("error/403.html")

@app.errorhandler(404)
def page_not_found(err):
    return render_template("error/404.html")



if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
