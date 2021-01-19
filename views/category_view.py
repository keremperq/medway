from flask import current_app, render_template, request, redirect, url_for
from views.equipment_view import take_equipment_ids_and_names_by_equipment, take_categories_by_equipment


def equipments_by_category_page(cat_id):
    db = current_app.config["db"]
    category = db.category.get_row(where_columns="CAT_ID", where_values=cat_id)
    if request.method == "GET":
        equipment_category_list = db.category.get_table(where_columns="CAT_ID", where_values=cat_id)
        equipments = []
        for equipment_category in equipment_category_list:
            equipments.append((db.equipment.get_row(equipment_category.eq_id), take_equipment_ids_and_names_by_equipment(equipment_category.eq_id), take_categories_by_equipment(equipment_category.eq_id)))
        return render_template("equipment/equipments.html", equipments=equipments, title="Equipments in category of " + category.cat_name)
    else:
        form_equipment_keys = request.form.getlist("equipment_keys")
        for form_equipment_key in form_equipment_keys:
            db.equipment.delete(form_equipment_key)
        return redirect(url_for("equipments_page"))


def categories_page():
    db = current_app.config["db"]
    categories = db.category.get_table()
    return render_template("category/categories.html", categories=categories)