from datetime import datetime, date
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange, ValidationError
from wtforms import StringField, TextAreaField, BooleanField, DateTimeField, validators, SubmitField, IntegerField

from wtforms.fields.html5 import DateField, DecimalRangeField, IntegerRangeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from pharmbase.models import Drug, Order
from pharmbase import app, db



class Searchbar(FlaskForm):
    search_string=StringField()
    submit= SubmitField('search')
      
class DrugForm(FlaskForm):
    name= StringField('Drug Name', [validators.DataRequired()])
    description = TextAreaField('Body')
    quantity = IntegerField(
        'Quantity',
        validators=[NumberRange(
            min=1,
            max=10000
        )]
    )
    expiry_date =  DateField('Expiring Date', [validators.DataRequired()])
    
    submit= SubmitField('Add Drug')
    

    def validate_name(self, name):
        drug= Drug.query.filter_by(name=name.data).first()
        if drug:
            raise ValidationError(f'{name.data} already exist')

    def validate_expiry_date(form, field):
        now= datetime.now().date()
        # print(field.data)
        if field.data <= now:
            raise ValidationError('Expiry Date should be ahead of today') 

class LocationForm(FlaskForm):
    name= StringField(label='Location', validators=[DataRequired()])
    submit= SubmitField('submit')

class MovementForm(FlaskForm):
    drug= StringField(label='Drug Name')
    location= StringField(label='Location', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit= SubmitField('Move Drug')