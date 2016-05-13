from flask_wtf import Form
from wtforms import SubmitField, SelectField

class SelectionForm(Form):
    drop = SelectField("Select")
    submit = SubmitField("Begin")

