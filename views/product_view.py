from table_operations.all_equipment.eq_cooler import Eq_cooler
from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import ProductObj, TransactionProductObj
from views.equipment_view import take_categories_by_equipment,  take_equipment_ids_and_names_by_equipment


def products_page():
    db = current_app.config["db"]
    if request.method == "GET":
        tables = db.product.get_products_all_info()
        return render_template("product/products.html", tables=tables)
    else:
        return redirect(url_for("products_page"))


def product_page(eq_id):
    db = current_app.config["db"]

    # Take product information
    equipment = db.equipment.get_row(eq_id)
    product = db.product.get_row(eq_id)
    equipment_names = take_equipment_ids_and_names_by_equipment(eq_id)
    categories = take_categories_by_equipment(eq_id)

    # If there is not product, or equipment with this equipment_key and abort 404 page
    if product is None or equipment is None:
        return abort(404)

    # If the product page is displayed
    if request.method == "GET":
        # Blank buying form
        buying_values = {}
        return render_template("product/product.html", title=(equipment.equipment_name+" Product Page"), product=product, equipment=equipment, equipments=equipment_names,s=equipment_names,categories=categories, buying_values=buying_values)
    # If it is added to shopping cart
    else:
        if not current_user.is_authenticated or not product.is_active:
            return abort(401)
        transaction = db.transaction.get_row(where_columns=["CUSTOMER_ID", "IS_COMPLETED"], where_values=[current_user.id, False])
        # Take values from buying form
        buying_values = {"piece": request.form["piece"]}

        transaction_product = TransactionProductObj(transaction.transaction_id, product.eq_id, buying_values["piece"], product.price)

        # Invalid input control
        err_message = Control().Input().buying(buying_values, transaction_product=transaction_product, product=product)
        if err_message:
            return render_template("product/product.html", title=(equipment.equipment_name+" Product Page"), product=product, equipment=equipment, equipments=equipment_names, categories=categories, buying_values=buying_values, err_message=err_message)

        # Add product to shopping cart
        if db.transaction_product.get_row(where_columns=["TRANSACTION_ID", "EQ_ID"], where_values=[transaction_product.transaction_id, transaction_product.eq_id]):
            db.transaction_product.update(update_columns=["PIECE"], new_values=[transaction_product.piece], where_columns=["TRANSACTION_ID", "EQ_ID"], where_values=[transaction_product.transaction_id, transaction_product.eq_id])
        else:
            db.transaction_product.add(transaction_product)

        return redirect(url_for("product_page", eq_id=eq_id))


@login_required
def product_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]

    equipments = []
    for equipment in db.equipment.get_table():
        equipments.append({'equipment': equipment, 'equipments': db.equipment.get_table(where_columns=db.equipment.columns["eq_id"], where_values=equipment.eq_id)})
    
    # If the product add page is displayed
    if request.method == "GET":
        values = {"equipment": "", "remaining": "", "price": "", "explanation": "", "is_active": ""}
        return render_template("product/product_form.html", title="Product Adding", values=values, equipments=equipments)
    # If product is added
    else:
        # Take values from buying form
        values = {"equipments": request.form["equipments"], "remaining": request.form["remaining"], "price": request.form["price"], "explanation": request.form["explanation"], "is_active": request.form.getlist("is_active") == ['active']}

        # Invalid input control
        err_message = Control().Input().product(values)
        if err_message:
            return render_template("product/product_form.html", title="Product Adding", values=values, equipments=equipments, err_message=err_message)

        product = ProductObj(values["equipments"].split()[0], values["equipments"].split()[1], values["remaining"], values["price"], 0, values["explanation"], values["is_active"])
        eq_id = db.product.add(product)
        return redirect(url_for("product_page",eq_id=eq_id))


@login_required
def product_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]

    # Take product information
    product = db.product.get_row(eq_id)
    # If there is no product with this equipment_key, abort 404 page
    if product is None:
        return abort(404)

    equipments = []
    for equipment in db.equipment.get_table():
        equipments.append({'equipment': equipment, 'equipments': db.equipment.get_table(where_columns=db.equipment.columns["eq_id"], where_values=equipment.eq_id)})

    # If the product add page is displayed
    if request.method == "GET":
        values = {"equipments": str(product.eq_id) , "remaining": product.remaining, "price": product.price, "explanation": product.explanation, "is_active": product.is_active}
        return render_template("product/product_form.html", title="Product Editing", values=values, equipments=equipments)
    # If product is added
    else:
        # Take values from buying form
        values = {"equipments": request.form["equipments"], "remaining": request.form["remaining"], "price": request.form["price"], "explanation": request.form["explanation"], "is_active": request.form.getlist("is_active") == ['active']}

        # Invalid input control
        err_message = Control().Input().product(values, is_new=False, equipments=str(product.eq_id))
        if err_message:
            return render_template("product/product_form.html", title="Product Editing", values=values, equipments=equipments, err_message=err_message)

        product = ProductObj(product.eq_id, values["remaining"], values["price"], product.number_of_sells, values["explanation"], values["is_active"])
        eq_id = db.product.update(product.eq_id, product)
        return redirect(url_for("product_page", eq_id=eq_id))


@login_required
def product_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    product = db.product.get_row(eq_id)
    product.is_active = False
    db.product.update(eq_id, product)
    return redirect(url_for("equipment_page", equipment_key=eq_id))