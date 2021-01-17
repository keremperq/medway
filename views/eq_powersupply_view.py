from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_powersupplyObj


def eq_powersupply_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_powersupply_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "power_w": "", "power_type": "", "sata_connection": ""}
        return render_template("eq_powersupply/eq_powersupply_form.html", values=values, title="Eq_powersupply Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'power_w': request.form["power_w"], 'power_type': request.form["power_type"], 'sata_connection': request.form["sata_connection"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_powersupply/eq_powersupply_form.html", values=values, title="Eq_powersupply Adding", equipments=equipments, err_message=err_message, add=True)

        eq_powersupply = Eq_powersupplyObj(values["eq_id"], values["power_w"], values["power_type"], values["sata_connection"])
        eq_id = db.eq_powersupply.add(eq_powersupply)
        return redirect(url_for("eq_powersupply_page", eq_id=eq_id))


@login_required
def eq_powersupply_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_powersupply = db.eq_powersupply.get_row(eq_id)
        if eq_powersupply is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_powersupply": eq_powersupply, "power_w": eq_powersupply.power_w, "power_type": eq_powersupply.power_type, "sata_connection": eq_powersupply.sata_connection}
        return render_template("eq_powersupply/eq_powersupply_form.html", values=values, title="Eq_powersupply Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_powersupply': request.form["eq_powersupply"], 'power_type': request.form["power_type"], 'sata_connection': request.form["sata_connection"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_powersupply/eq_powersupply_form.html", values=values, title="Eq_powersupply Editing", equipments=equipments, err_message=err_message, add=False)

        eq_powersupply = Eq_powersupplyObj(values["eq_id"], values["power_w"], values["power_type"], values["sata_connection"])
        eq_id = db.eq_powersupply.update(eq_id, eq_powersupply)
        return redirect(url_for("eq_powersupply_page", eq_id=eq_id))


@login_required
def eq_powersupply_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_powersupply.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))