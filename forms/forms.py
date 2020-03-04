from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, validators
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class ParkingForm(FlaskForm):
    name = StringField('Parking name', validators=[DataRequired()])
    address = StringField('Parking address', validators=[DataRequired()])
    price = IntegerField('Cost of monthly rent', validators=[DataRequired()])



class RentalForm(FlaskForm):
    beg_date = DateField('Date of rent begining', validators=[DataRequired()])
    price = IntegerField('Cost of monthly rent', validators=[DataRequired()])
    renter_name = StringField('Renter name', validators=[DataRequired()])
    renter_mob_num = StringField('Renter mobile number',
                                validators=[DataRequired()])
    parking_name = StringField('Parking name', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
