

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    name = StringField("Your name :", validators=[DataRequired()])
    role = SelectMultipleField("role", choices=[(1, "admin"), (2, "honor"), (3, "user")], coerce=int)
    submit = SubmitField("Envoyer")


