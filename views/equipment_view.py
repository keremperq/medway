from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import EquipmentObj, CommentObj
from views.comment_view import take_comments_with_and_by


def equipments_page():
    db = current_app.config["db"]
    if request.method == "GET":
        equipments = []
        for equipment in db.equipment.get_table():
            equipments.append((equipment, take_categories_by_equipment(equipment.eq_id)))
        return render_template("equipment/equipments.html", equipments=equipments, title="All equipments")
    else:
        form_equipment_keys = request.form.getlist("equipment_keys")
        for form_equipment_key in form_equipment_keys:
            db.equipment.delete(form_equipment_key)
        return redirect(url_for("equipments_page"))


def equipment_page(equipment_key):
    db = current_app.config["db"]

    # Take equipment information
    equipment = db.equipment.get_row(equipment_key)
    # If there is no equipment with this equipment_key, abort 404 page
    if equipment is None:
        return abort(404)

    # Take equipment and comments of this equipment
    equipments = db.equipment.get_row(equipment_key)
    comments = take_comments_with_and_by(eq_id=equipment_key)
    categories = take_categories_by_equipment(equipment_key)

    # If the equipment page is displayed
    if request.method == "GET":
        # Blank comment form
        new_comment_values = {"comment_title": "", "comment_statement": ""}
        return render_template("equipment/equipment.html", equipments=equipments, comments=comments, new_comment_values=new_comment_values, categories=categories)
    # If the new comment is added
    else:
        if not current_user.is_authenticated:
            return abort(401)
        # Take values from add_comment form
        new_comment_values = {"customer_id": current_user.id, "eq_id": equipment_key, "comment_title": request.form["comment_title"], "comment_statement": request.form["comment_statement"]}

        comment_err_message = Control().Input().comment(new_comment_values)
        if comment_err_message:
            return render_template("equipment/equipment.html", equipment=equipment, comments=comments, comment_err_message=comment_err_message, new_comment_values=new_comment_values, categories=categories)

        # Add comment to database
        comment = CommentObj(new_comment_values["customer_id"], new_comment_values["eq_id"], new_comment_values["comment_title"], new_comment_values["comment_statement"])
        db.comment.add(comment)

        return redirect(url_for("equipment_page", equipment_key=equipment_key))


@login_required
def equipment_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    
    # Get categories
    categories = db.category.get_table()

    if request.method == "GET":
        values = {"eq_name": "", "eq_brand": "","selected_category_ids": []}
        return render_template("equipment/equipment_form.html", values=values, title="Equipment adding", err_message=err_message, categories=categories)
    else:
        values = {"eq_name": request.form["eq_name"], "eq_brand": request.form["eq_brand"],"selected_category_ids": request.form.getlist("selected_category_ids")}

        # Invalid input control
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("equipment/equipment_form.html", values=values, title="Equipment adding", err_message=err_message, categories=categories)

        equipment = EquipmentObj(None, values["eq_name"], values["eq_brand"])

        db.equipment.add_equipment(equipment)

        return redirect(url_for("equipments_page"))


@login_required
def equipment_edit_page(equipment_key):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    # Get categories
    categories = db.category.get_table()

    if request.method == "GET":
        equipment = db.equipment.get_row(equipment_key)
        if equipment is None:
            return abort(404)

        selected_category_ids = []
        for category in db.equipment.get_table(where_columns="EQ_ID", where_values=equipment.eq_id):
            selected_category_ids.append(category.cat_id)

        values = {"eq_name": equipment.eq_name, "eq_brand": equipment.eq_brand, "eq_image": equipment.eq_image, "selected_category_ids": selected_category_ids}
        return render_template("equipment/equipment_form.html", values=values, title="Equipment editing", err_message=err_message, categories=categories)
    else:
        values = {"eq_name": request.form["eq_name"], "eq_brand": request.form["eq_brand"], "eq_image": request.form["eq_image"],"selected_category_ids": request.form.getlist("selected_category_ids")}

        # Invalid input control
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("equipment/equipment_form.html", values=values, title="Equipment adding", err_message=err_message, categories=categories)

        equipment = EquipmentObj(None, values["eq_name"], values["eq_brand"], values["eq_image"], values["cat_id"])
        eq_id = db.equipment.update(equipment_key, equipment)

        db.equipment.delete(where_columns="EQ_ID", where_values=[eq_id])
        for category_id in values["selected_category_ids"]:
            db.equipment.add(eq_id, category_id)
        return redirect(url_for("equipment_page", equipment_key=equipment_key))


@login_required
def equipment_delete_page(equipment_key):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.equipment.delete(equipment_key)
    return redirect(url_for("equipments_page"))


def take_categories_by_equipment(eq_id):
    db = current_app.config["db"]
    categories = []
    for equipment_category in db.equipment.get_table(where_columns="EQ_ID", where_values=eq_id):
        categories.append(db.equipment.get_row(where_columns="CAT_ID", where_values=equipment_category.cat_id))
    return categories
