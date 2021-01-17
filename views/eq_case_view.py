from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_caseObj


def eq_case_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_case_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "case_type": "", "has_audio": "", "is_transparent": "", "has_psu": ""}
        return render_template("eq_case/eq_case_form.html", values=values, title="Eq_case Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'case_type': request.form["case_type"], 'has_audio': request.form["has_audio"], 'is_transparent': request.form["is_transparent"], 'has_psu': request.form["has_psu"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_case/eq_case_form.html", values=values, title="Eq_case Adding", equipments=equipments, err_message=err_message, add=True)

        eq_case = Eq_caseObj(values["eq_id"], values["case_type"], values["has_audio"], values["is_transparent"], values["has_psu"])
        eq_id = db.eq_case.add(eq_case)
        return redirect(url_for("eq_case_page", eq_id=eq_id))


@login_required
def eq_case_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_case = db.eq_case.get_row(eq_id)
        if eq_case is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_case": eq_case, "case_type": eq_case.case_type, "has_audio": eq_case.has_audio, "is_transparent": eq_case.is_transparent, "has_psu": eq_case.has_psu}
        return render_template("eq_case/eq_case_form.html", values=values, title="Eq_case Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_case': request.form["eq_case"], 'has_audio': request.form["has_audio"], 'is_transparent': request.form["is_transparent"], 'has_psu': request.form["has_psu"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_case/eq_case_form.html", values=values, title="Eq_case Editing", equipments=equipments, err_message=err_message, add=False)

        eq_case = Eq_caseObj(values["eq_id"], values["case_type"], values["has_audio"], values["is_transparent"], values["has_psu"])
        eq_id = db.eq_case.update(eq_id, eq_case)
        return redirect(url_for("eq_case_page", eq_id=eq_id))


@login_required
def eq_case_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_case.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))