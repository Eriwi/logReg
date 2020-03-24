from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.validators import data_required


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[data_required()])
    password = PasswordField('Password', validators=[data_required()])


class CompanyForm(FlaskForm):
    company_name = StringField('Company name', validators=[data_required()])
    confirm = BooleanField('Check this', validators=[data_required()])


class OrderForm(FlaskForm):
    order_reference = StringField('Order Reference', validators=[data_required()])
    company = SelectField('Company', coerce=int, validators=[data_required()])


class ArticleForm(FlaskForm):
    time = IntegerField('Time in minutes', validators=[data_required()])
    order = SelectField('Order', coerce=int, validators=[data_required()])
