from flask import current_app

class Control:
    class Input:
        @staticmethod
        def equipment(values):
            err_message = None
            db = current_app.config["db"]

            # Invalid input control
            if len(values["explanation"]) >= 1000:
                err_message = "Explanation cannot be more than 1000 character"
            elif len(values["eq_name"]) >= 100:
                err_message = "Equipment name cannot be more than 100 character"

            for cat_id in values["selected_category_ids"]:
                if not db.category.get_row(where_columns=["CAT_ID"], where_values=[cat_id]):
                    err_message = "Please select category from list"
                    return err_message

            return err_message


        @staticmethod
        def comment(values):
            err_message = None
            db = current_app.config["db"]

            # Invalid input control
            if not db.customer.get_row(where_columns="CUSTOMER_ID", where_values=str(values["customer_id"])):
                err_message = "There is no customer with this customer_id"
            elif not db.equipment.get_row(values["eq_id"]):
                err_message = "There is no equipment with this eq_id"
            elif len(values["comment_title"]) >= 50:
                err_message = "Comment title cannot be more than 50 character"
            elif len(values["comment_statement"]) >= 500:
                err_message = "Comment statement cannot be more than 500 character"

            return err_message

        @staticmethod
        def buying(values, transaction_product, product):
            err_message = None

            # Invalid input control
            if int(product.remaining) < int(values["piece"]):
                err_message = "There is no enough product"

            return err_message

        @staticmethod
        def product(values, equipment=None, is_new=True):
            err_message = None
            db = current_app.config["db"]

            # Invalid input control
            if equipment is not None and equipment != values["equipment"]:
                err_message = "Equipment ID and cannot changed"
            elif is_new and db.product.get_row(values["equipment"].split()[0], values["equipment"].split()[1]):
                err_message = "This product is already attached, please try editing."
            elif not db.equipment.get_row(values["equipment"].split()[0], values["equipment"].split()[1]):
                err_message = "Invalid equipment ID"
            elif int(values["remaining"]) < 0:
                err_message = "Remaining must be equal or greater than 0"
            elif float(values["price"]) < 0:
                err_message = "Price cannot be lower than 0"
            elif len(values["explanation"]) > 500:
                err_message = "Explanation cannot be more than 500 character"

            return err_message

        @staticmethod
        def transaction(values, transaction):
            err_message = None
            db = current_app.config["db"]

            # Invalid input control
            if not db.transaction.get_row(where_columns=["CUSTOMER_ID", "ADDRESS_ID"], where_values=[transaction.customer_id, values["address_id"]]):
                err_message = "This address does not belong to the customer."
            elif len(values["payment_type"]) > 30:
                err_message = "Payment type cannot be more than 30 character"
            elif len(values["transaction_explanation"]) > 500:
                err_message = "Explanation cannot be more than 500 character"

            return err_message