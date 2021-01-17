from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_videocardObj


def eq_videocard_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_videocard_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "memory_size": "", "core_speed": "", "gpu_model": "", "manufacturer": ""}
        return render_template("eq_videocard/eq_videocard_form.html", values=values, title="Eq_videocard Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'memory_size': request.form["memory_size"], 'core_speed': request.form["core_speed"], 'gpu_model': request.form["gpu_model"], 'manufacturer': request.form["manufacturer"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_videocard/eq_videocard_form.html", values=values, title="Eq_videocard Adding", equipments=equipments, err_message=err_message, add=True)

        eq_videocard = Eq_videocardObj(values["eq_id"], values["memory_size"], values["core_speed"], values["gpu_model"], values["manufacturer"])
        eq_id = db.eq_videocard.add(eq_videocard)
        return redirect(url_for("eq_videocard_page", eq_id=eq_id))


@login_required
def eq_videocard_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_videocard = db.eq_videocard.get_row(eq_id)
        if eq_videocard is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_videocard": eq_videocard, "memory_size": eq_videocard.memory_size, "core_speed": eq_videocard.core_speed, "gpu_model": eq_videocard.gpu_model, "manufacturer": eq_videocard.manufacturer}
        return render_template("eq_videocard/eq_videocard_form.html", values=values, title="Eq_videocard Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_videocard': request.form["eq_videocard"], 'core_speed': request.form["core_speed"], 'gpu_model': request.form["gpu_model"], 'manufacturer': request.form["manufacturer"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_videocard/eq_videocard_form.html", values=values, title="Eq_videocard Editing", equipments=equipments, err_message=err_message, add=False)

        eq_videocard = Eq_videocardObj(values["eq_id"], values["memory_size"], values["core_speed"], values["gpu_model"], values["manufacturer"])
        eq_id = db.eq_videocard.update(eq_id, eq_videocard)
        return redirect(url_for("eq_videocard_page", eq_id=eq_id))


@login_required
def eq_videocard_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_videocard.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))