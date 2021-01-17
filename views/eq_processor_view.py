from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_processorObj


def eq_processor_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_processor_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "model": "", "fre_speed": "", "core_number": ""}
        return render_template("eq_processor/eq_processor_form.html", values=values, title="Eq_processor Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'model': request.form["model"], 'fre_speed': request.form["fre_speed"], 'core_number': request.form["core_number"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_processor/eq_processor_form.html", values=values, title="Eq_processor Adding", equipments=equipments, err_message=err_message, add=True)

        eq_processor = Eq_processorObj(values["eq_id"], values["model"], values["fre_speed"], values["core_number"])
        eq_id = db.eq_processor.add(eq_processor)
        return redirect(url_for("eq_processor_page", eq_id=eq_id))


@login_required
def eq_processor_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_processor = db.eq_processor.get_row(eq_id)
        if eq_processor is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_processor": eq_processor, "model": eq_processor.model, "fre_speed": eq_processor.fre_speed, "core_number": eq_processor.core_number}
        return render_template("eq_processor/eq_processor_form.html", values=values, title="Eq_processor Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_processor': request.form["eq_processor"], 'fre_speed': request.form["fre_speed"], 'core_number': request.form["core_number"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_processor/eq_processor_form.html", values=values, title="Eq_processor Editing", equipments=equipments, err_message=err_message, add=False)

        eq_processor = Eq_processorObj(values["eq_id"], values["model"], values["fre_speed"], values["core_number"])
        eq_id = db.eq_processor.update(eq_id, eq_processor)
        return redirect(url_for("eq_processor_page", eq_id=eq_id))


@login_required
def eq_processor_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_processor.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))