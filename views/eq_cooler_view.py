from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_coolerObj


def eq_cooler_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_cooler_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "cooler_type": "", "cooler_size": "", "led_color": ""}
        return render_template("eq_cooler/eq_cooler_form.html", values=values, title="Eq_cooler Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'cooler_type': request.form["cooler_type"], 'cooler_size': request.form["cooler_size"], 'led_color': request.form["led_color"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_cooler/eq_cooler_form.html", values=values, title="Eq_cooler Adding", equipments=equipments, err_message=err_message, add=True)

        eq_cooler = Eq_coolerObj(values["eq_id"], values["cooler_type"], values["cooler_size"], values["led_color"])
        eq_id = db.eq_cooler.add(eq_cooler)
        return redirect(url_for("eq_cooler_page", eq_id=eq_id))


@login_required
def eq_cooler_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_cooler = db.eq_cooler.get_row(eq_id)
        if eq_cooler is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_cooler": eq_cooler, "cooler_type": eq_cooler.cooler_type, "cooler_size": eq_cooler.cooler_size, "led_color": eq_cooler.led_color}
        return render_template("eq_cooler/eq_cooler_form.html", values=values, title="Eq_cooler Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_cooler': request.form["eq_cooler"], 'cooler_size': request.form["cooler_size"], 'led_color': request.form["led_color"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_cooler/eq_cooler_form.html", values=values, title="Eq_cooler Editing", equipments=equipments, err_message=err_message, add=False)

        eq_cooler = Eq_coolerObj(values["eq_id"], values["cooler_type"], values["cooler_size"], values["led_color"])
        eq_id = db.eq_cooler.update(eq_id, eq_cooler)
        return redirect(url_for("eq_cooler_page", eq_id=eq_id))


@login_required
def eq_cooler_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_cooler.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))