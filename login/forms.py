from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired


class SignupForm(Form):
    email = StringField('email',
                validators=[DataRequired(), Email()])
    password = PasswordField(
                'Password',
                validators=[DataRequired()])
    first_name = StringField(
                'First Name',
                validators=[DataRequired()])
    last_name = StringField(
                'Last Name',
                validators=[DataRequired()])
    middle_name = StringField(
                'Middle Name',
                validators=[DataRequired()])
    cell_phone = StringField(
                'Cell Phone',
                validators=[DataRequired()])
    street_address = StringField(
                'Street Address',
                validators=[DataRequired()])
    city = StringField(
                'City',
                validators=[DataRequired()])
    zip_code = StringField(
                'Zip Code',
                validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(Form):
    email = StringField('email',
                validators=[DataRequired(), Email()])
    password = PasswordField(
                'Password',
                validators=[DataRequired()])
    submit = SubmitField("Sign In")