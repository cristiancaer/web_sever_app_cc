from flask_wtf import FlaskForm
from wtforms.fields import FloatField,SubmitField
from wtforms.validators import DataRequired
# info 
separator="---"
class PutForm(FlaskForm):
    mass_flow=FloatField('mass_flow',validators=[DataRequired()])
    humidity=FloatField('humidity')
    sent=SubmitField()
