from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_headsetObj


def eq_headset_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_headset_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "usage_area": "", "headset_type": "", "has_mic": ""}
        return render_template("eq_headset/eq_headset_form.html", values=values, title="Eq_headset Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'usage_area': request.form["usage_area"], 'headset_type': request.form["headset_type"], 'has_mic': request.form["has_mic"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_headset/eq_headset_form.html", values=values, title="Eq_headset Adding", equipments=equipments, err_message=err_message, add=True)

        eq_headset = Eq_headsetObj(values["eq_id"], values["usage_area"], values["headset_type"], values["has_mic"])
        eq_id = db.eq_headset.add(eq_headset)
        return redirect(url_for("eq_headset_page", eq_id=eq_id))


@login_required
def eq_headset_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_headset = db.eq_headset.get_row(eq_id)
        if eq_headset is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_headset": eq_headset, "usage_area": eq_headset.usage_area, "headset_type": eq_headset.headset_type, "has_mic": eq_headset.has_mic}
        return render_template("eq_headset/eq_headset_form.html", values=values, title="Eq_headset Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_headset': request.form["eq_headset"], 'headset_type': request.form["headset_type"], 'has_mic': request.form["has_mic"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_headset/eq_headset_form.html", values=values, title="Eq_headset Editing", equipments=equipments, err_message=err_message, add=False)

        eq_headset = Eq_headsetObj(values["eq_id"], values["usage_area"], values["headset_type"], values["has_mic"])
        eq_id = db.eq_headset.update(eq_id, eq_headset)
        return redirect(url_for("eq_headset_page", eq_id=eq_id))


@login_required
def eq_headset_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_headset.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))