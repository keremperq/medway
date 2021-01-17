from flask import current_app, abort, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control


@login_required
def comments_page():
    if not current_user.is_admin:
        return abort(401)
    comments = take_comments_with_and_by(with_eq=True)
    return render_template("comment/comments.html", comments=comments)


@login_required
def comment_edit_page(comment_id):
    db = current_app.config["db"]

    # Take comment information and if there is no comment with comment id, abort 404 page
    comment = db.comment.get_row(comment_id)
    if comment is None:
        return abort(404)
    elif current_user.id != comment.customer_id:
        return abort(401)

    if request.method == "GET":
        values = {"comment_title": comment.comment_title, "comment_statement": comment.comment_statement}
        return render_template("comment/comment_form.html", title="Comment editing", comment_values=values)
    else:
        values = {"customer_id": comment.customer_id, "eq_id": comment.eq_id, "comment_title": request.form["comment_title"], "comment_statement": request.form["comment_statement"]}

        # Invalid input control
        err_message = Control().Input().comment(values)
        if err_message:
            return render_template("equipment/equipment.html", title="Comment editing", comment_values=values, err_message=err_message)

        # Update comment variable
        comment.comment_title = values["comment_title"]
        comment.comment_statement = values["comment_statement"]
        # Update comment in database
        db.comment.update(comment.comment_id, comment)

        return redirect(url_for("equipment_page", equipment_key=comment.eq_id))


@login_required
def comment_delete_page(comment_id):
    db = current_app.config["db"]

    # Take comment information and if there is no comment with comment id, abort 404 page
    comment = db.comment.get_row(comment_id)
    if comment is None:
        return abort(404)
    elif current_user.id != comment.customer_id and not current_user.is_admin:
        return abort(401)

    db.comment.delete(comment_id)
    return redirect(url_for("equipment_page", equipment_key=comment.eq_id))


def take_comments_with_and_by(eq_id=None, with_eq=False):
    db = current_app.config["db"]
    comments = []
    if with_eq:
        for comment in db.comment.get_table(eq_id=eq_id):
            comments.append((comment, db.customer.get_row(where_columns="CUSTOMER_ID", where_values=comment.customer_id), db.equipment.get_row(comment.eq_id)))
    else:
        for comment in db.comment.get_table(eq_id=eq_id):
            comments.append((comment, db.customer.get_row(where_columns="CUSTOMER_ID", where_values=comment.customer_id)))

    return comments