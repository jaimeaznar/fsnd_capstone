from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, AnyOf, URL
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import Company, Product


class ProductForm(Form):
    name = StringField('name', validators=[InputRequired()])
    image = FileField('image', validators=[FileAllowed(['png', 'jpg','jpeg'], 'png,jpg or jpeg files only!')])
    description = StringField('description', validators=[InputRequired()])

    def get_company_choices():      
        return Company.query

    company = QuerySelectField(query_factory=get_company_choices, validators=[InputRequired()],get_label='name')

class CompanyForm(Form):
    name = StringField('name', validators=[InputRequired()])
    city = StringField('city', validators=[InputRequired()])
    state = StringField('state', validators=[InputRequired()])
    address = StringField('address', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
