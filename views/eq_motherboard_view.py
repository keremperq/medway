from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_motherboardObj


def eq_motherboard_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_motherboard_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "ram_type": "", "max_ram": "", "ram_slot_number": "", "socket_type": "", "ram_fre_speed": ""}
        return render_template("eq_motherboard/eq_motherboard_form.html", values=values, title="Eq_motherboard Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'ram_type': request.form["ram_type"], 'max_ram': request.form["max_ram"], 'ram_slot_number': request.form["ram_slot_number"], 'socket_type': request.form["socket_type"],'ram_fre_speed': request.form["ram_fre_speed"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_motherboard/eq_motherboard_form.html", values=values, title="Eq_motherboard Adding", equipments=equipments, err_message=err_message, add=True)

        eq_motherboard = Eq_motherboardObj(values["eq_id"], values["ram_type"], values["max_ram"], values["ram_slot_number"], values["socket_type"], values["ram_fre_speed"])
        eq_id = db.eq_motherboard.add(eq_motherboard)
        return redirect(url_for("eq_motherboard_page", eq_id=eq_id))


@login_required
def eq_motherboard_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_motherboard = db.eq_motherboard.get_row(eq_id)
        if eq_motherboard is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_motherboard": eq_motherboard, "ram_type": eq_motherboard.ram_type, "max_ram": eq_motherboard.max_ram, "ram_slot_number": eq_motherboard.ram_slot_number, "socket_type": eq_motherboard.socket_type}
        return render_template("eq_motherboard/eq_motherboard_form.html", values=values, title="Eq_motherboard Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_motherboard': request.form["eq_motherboard"], 'max_ram': request.form["max_ram"], 'ram_slot_number': request.form["ram_slot_number"], 'socket_type': request.form["socket_type"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_motherboard/eq_motherboard_form.html", values=values, title="Eq_motherboard Editing", equipments=equipments, err_message=err_message, add=False)

        eq_motherboard = Eq_motherboardObj(values["eq_id"], values["ram_type"], values["max_ram"], values["ram_slot_number"], values["socket_type"], values["ram_fre_speed"])
        eq_id = db.eq_motherboard.update(eq_id, eq_motherboard)
        return redirect(url_for("eq_motherboard_page", eq_id=eq_id))


@login_required
def eq_motherboard_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_motherboard.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))