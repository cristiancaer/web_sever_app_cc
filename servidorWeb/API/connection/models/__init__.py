from flask_wtf import FlaskForm
from wtforms.fields import FloatField,SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired
# info 
separator="---"
class PutFlowForm(FlaskForm):
    mass_flow=FloatField('mass_flow',validators=[DataRequired()])
    sent=SubmitField()
    
class PutHumidityForm(FlaskForm):
    humidity=FloatField('humidity',validators=[DataRequired()])
    sent=SubmitField()
class ClearVarsForm(FlaskForm):
    password=PasswordField('password',validators=[DataRequired()])
    sent=SubmitField()
