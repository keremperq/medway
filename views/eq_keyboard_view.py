from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import Eq_keyboardObj


def eq_keyboard_page(eq_id):
    return redirect(url_for('equipment_page', equipment_key=eq_id))


@login_required
def eq_keyboard_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        values = {"eq_id": "", "keyboard_type": "", "key_sequece": "", "is_mechanic": "", "is_rgb": ""}
        return render_template("eq_keyboard/eq_keyboard_form.html", values=values, title="Eq_keyboard Adding", equipments=equipments, err_message=err_message, add=True)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'keyboard_type': request.form["keyboard_type"], 'key_sequece': request.form["key_sequece"], 'is_mechanic': request.form["is_mechanic"], 'is_rgb': request.form["is_rgb"]}
        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_keyboard/eq_keyboard_form.html", values=values, title="Eq_keyboard Adding", equipments=equipments, err_message=err_message, add=True)

        eq_keyboard = Eq_keyboardObj(values["eq_id"], values["keyboard_type"], values["key_sequece"], values["is_mechanic"], values["is_rgb"])
        eq_id = db.eq_keyboard.add(eq_keyboard)
        return redirect(url_for("eq_keyboard_page", eq_id=eq_id))


@login_required
def eq_keyboard_edit_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    err_message = None
    equipments = db.equipment.get_table()
    if request.method == "GET":
        eq_keyboard = db.eq_keyboard.get_row(eq_id)
        if eq_keyboard is None:
            return abort(404)
        values = {"eq_id": eq_id, "eq_keyboard": eq_keyboard, "keyboard_type": eq_keyboard.keyboard_type, "key_sequece": eq_keyboard.key_sequece, "is_mechanic": eq_keyboard.is_mechanic, "is_rgb": eq_keyboard.is_rgb}
        return render_template("eq_keyboard/eq_keyboard_form.html", values=values, title="Eq_keyboard Editing", equipments=equipments, err_message=err_message, add=False)
    else:
        values = {'eq_id': int(request.form["eq_id"]), 'eq_keyboard': request.form["eq_keyboard"], 'key_sequece': request.form["key_sequece"], 'is_mechanic': request.form["is_mechanic"], 'is_rgb': request.form["is_rgb"]}

        err_message = Control().Input().equipment(values)
        if err_message:
            return render_template("eq_keyboard/eq_keyboard_form.html", values=values, title="Eq_keyboard Editing", equipments=equipments, err_message=err_message, add=False)

        eq_keyboard = Eq_keyboardObj(values["eq_id"], values["keyboard_type"], values["key_sequece"], values["is_mechanic"], values["is_rgb"])
        eq_id = db.eq_keyboard.update(eq_id, eq_keyboard)
        return redirect(url_for("eq_keyboard_page", eq_id=eq_id))


@login_required
def eq_keyboard_delete_page(eq_id):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    db.eq_keyboard.delete(eq_id)
    return redirect(url_for("equipment_page", eq_key=eq_id))