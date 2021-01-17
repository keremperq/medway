from Flask_WTF import FlaskForm
from WTForms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from WTForms.validators import InputRequired, Length, Email, Optional


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired("Please enter your username"), Length(5, 30)], id='username')
    password = PasswordField("Password", validators=[InputRequired("Please enter your password"), Length(6, 20)], id='password')
    remember_me = BooleanField("Remember me", default=False, id='remember_me')
    submit = SubmitField("Login")


class CustomerForm(FlaskForm):
    c_name = StringField("Name", validators=[InputRequired("Please enter author's name"), Length(1, 30, "Name can not be longer than %(max)d character")], id='customer_name')
    c_surname = StringField("Surname", validators=[InputRequired("Please enter author's surname"), Length(1, 30, "Surname can not be longer than %(max)d character")], id='surname')
    

class SignUpForm(CustomerForm):
    c_username = StringField("Username", validators=[InputRequired("Please enter your username"), Length(5, 30, "Username length must be between %(min)d and %(max)d character")], id='customer_username')
    c_email = StringField("E-mail", validators=[Email("You must provide a valid mail address"), Length(3, 50, "Email can not be longer than %(max)d character")], id='customer_email')
    c_password = PasswordField("Password", validators=[InputRequired("Please enter your password"), Length(6, 20, "Password length must be between %(min)d and %(max)d character")], id='customer_password')
    c_phone = StringField("Phone", validators=[InputRequired("Please enter your phone number"), Length(8, 10, "Phone number must be between %(min)d and %(max)d length")], id='customer_phone')
    submit = SubmitField("Sign up")

class AddressForm(FlaskForm):
    address_name = StringField("Address name", validators=[InputRequired("Please enter address' name"), Length(1, 30, "Address name can not be longer than %(max)d character")], id='address_name')
    country = StringField("Country", validators=[InputRequired("Please enter country"), Length(1, 30, "Country can not be longer than %(max)d character")], id='country')
    city = StringField("City", validators=[InputRequired("Please enter city"), Length(1, 30, "City can not be longer than %(max)d character")], id='city')
    neighborhood = StringField("Neighborhood", validators=[InputRequired("Please enter neighborhood"), Length(1, 30, "Neighborhood can not be longer than %(max)d character")], id='neighborhood')
    street = StringField("Street", validators=[InputRequired("Please enter street"), Length(1, 30, "Street can not be longer than %(max)d character")], id='street')
    address_no = StringField("Number", validators=[InputRequired("Please enter number"), Length(1, 10, "Address number can not be longer than %(max)d character")], id='address_no')
    zipcode = StringField("Zipcode", validators=[InputRequired("Please enter zipcode"), Length(1, 5, "Zipcode can not be longer than %(max)d character")], id='zipcode')
    explanation = TextAreaField("Explanation", validators=[Optional(), Length(1, 500, "Explanation can not be longer than %(max)d character")], id='explanation')
    submit = SubmitField("Add Address")