from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_ramObj


def eq_ram_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_ram_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "ram_type": "", "capacity": "", "fre_speed": ""}
        return render_template("eq_ram/eq_ram_form.html", values=values, title="Eq_ram Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'ram_type': request.form["ram_type"], 'capacity': request.form["capacity"], 'fre_speed': request.form["fre_speed"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_ram/eq_ram_form.html", values=values, title="Eq_ram Adding", equipments=equipments, err_message=err_message, add=True)

        eq_ram = Eq_ramObj(values["eq_id"], values["ram_type"], values["capacity"], values["fre_speed"])
        eq_id = db.eq_ram.add(eq_ram)
        return redirect(url_for("eq_ram_page", eq_id=eq_id))


@login_required
def eq_ram_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_ram = db.eq_ram.get_row(eq_id)
        if eq_ram is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_ram": eq_ram, "ram_type": eq_ram.ram_type, "capacity": eq_ram.capacity, "fre_speed": eq_ram.fre_speed}
        return render_template("eq_ram/eq_ram_form.html", values=values, title="Eq_ram Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_ram': request.form["eq_ram"], 'capacity': request.form["capacity"], 'fre_speed': request.form["fre_speed"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_ram/eq_ram_form.html", values=values, title="Eq_ram Editing", equipments=equipments, err_message=err_message, add=False)

        eq_ram = Eq_ramObj(values["eq_id"], values["ram_type"], values["capacity"], values["fre_speed"])
        eq_id = db.eq_ram.update(eq_id, eq_ram)
        return redirect(url_for("eq_ram_page", eq_id=eq_id))


@login_required
def eq_ram_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_ram.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))