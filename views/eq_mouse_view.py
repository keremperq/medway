from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_mouseObj


def eq_mouse_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_mouse_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "mouse_type": "", "dpi": "", "buttons": ""}
        return render_template("eq_mouse/eq_mouse_form.html", values=values, title="Eq_mouse Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'mouse_type': request.form["mouse_type"], 'dpi': request.form["dpi"], 'buttons': request.form["buttons"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_mouse/eq_mouse_form.html", values=values, title="Eq_mouse Adding", equipments=equipments, err_message=err_message, add=True)

        eq_mouse = Eq_mouseObj(values["eq_id"], values["mouse_type"], values["dpi"], values["buttons"])
        eq_id = db.eq_mouse.add(eq_mouse)
        return redirect(url_for("eq_mouse_page", eq_id=eq_id))


@login_required
def eq_mouse_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_mouse = db.eq_mouse.get_row(eq_id)
        if eq_mouse is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_mouse": eq_mouse, "mouse_type": eq_mouse.mouse_type, "dpi": eq_mouse.dpi, "buttons": eq_mouse.buttons}
        return render_template("eq_mouse/eq_mouse_form.html", values=values, title="Eq_mouse Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_mouse': request.form["eq_mouse"], 'dpi': request.form["dpi"], 'buttons': request.form["buttons"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_mouse/eq_mouse_form.html", values=values, title="Eq_mouse Editing", equipments=equipments, err_message=err_message, add=False)

        eq_mouse = Eq_mouseObj(values["eq_id"], values["mouse_type"], values["dpi"], values["buttons"])
        eq_id = db.eq_mouse.update(eq_id, eq_mouse)
        return redirect(url_for("eq_mouse_page", eq_id=eq_id))


@login_required
def eq_mouse_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_mouse.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))