from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, RadioField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class SearchStanding(Form):
    entity_type = RadioField('Entity Type',
                             choices=[('alliance', 'Alliance'), ('corporation', 'Corporation')],
                             default='alliance',
                             validators=[DataRequired()])
    search_text = StringField('Search', validators=[DataRequired()])
    standing = RadioField('Standing',
                          choices=[('+10', '+10'), ('+5', '+5'), ('+2.5', '+2.5'), ('+1.1', '+1.1'), ('0', '0'), ('-5', '-5'), ('-10', '-10')],
                          default='+2.5',
                          validators=[DataRequired()])
    add_by_id = SubmitField('Add By Id')
    add_by_name = SubmitField('Add By Name')
    add_by_ticker = SubmitField('Add By Ticker')

class ConfirmStanding(Form):
    entity_type = HiddenField('Entity Type', validators=[DataRequired()])
    standing = HiddenField('Search', validators=[DataRequired()])
