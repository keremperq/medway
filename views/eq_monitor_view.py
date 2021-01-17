from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_monitorObj


def eq_monitor_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_monitor_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "screen_size": "", "resolution": "", "refresh_rate": ""}
        return render_template("eq_monitor/eq_monitor_form.html", values=values, title="Eq_monitor Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'screen_size': request.form["screen_size"], 'resolution': request.form["resolution"], 'refresh_rate': request.form["refresh_rate"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_monitor/eq_monitor_form.html", values=values, title="Eq_monitor Adding", equipments=equipments, err_message=err_message, add=True)

        eq_monitor = Eq_monitorObj(values["eq_id"], values["screen_size"], values["resolution"], values["refresh_rate"])
        eq_id = db.eq_monitor.add(eq_monitor)
        return redirect(url_for("eq_monitor_page", eq_id=eq_id))


@login_required
def eq_monitor_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_monitor = db.eq_monitor.get_row(eq_id)
        if eq_monitor is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_monitor": eq_monitor, "screen_size": eq_monitor.screen_size, "resolution": eq_monitor.resolution, "refresh_rate": eq_monitor.refresh_rate}
        return render_template("eq_monitor/eq_monitor_form.html", values=values, title="Eq_monitor Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_monitor': request.form["eq_monitor"], 'resolution': request.form["resolution"], 'refresh_rate': request.form["refresh_rate"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_monitor/eq_monitor_form.html", values=values, title="Eq_monitor Editing", equipments=equipments, err_message=err_message, add=False)

        eq_monitor = Eq_monitorObj(values["eq_id"], values["screen_size"], values["resolution"], values["refresh_rate"])
        eq_id = db.eq_monitor.update(eq_id, eq_monitor)
        return redirect(url_for("eq_monitor_page", eq_id=eq_id))


@login_required
def eq_monitor_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_monitor.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))