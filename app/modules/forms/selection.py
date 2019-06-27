from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.widgets import ListWidget, CheckboxInput
from app.modules.queries.instruments import get_all_instruments


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class InstrumentSelectionForm(FlaskForm):
    start_dt = DateField('DatePicker', format='%Y-%m-%d')
    end_dt = DateField('DatePicker', format='%Y-m%-%d')
    instrument = SelectField(label='Instrument', choices=get_all_instruments())
    vwap_checkbox = BooleanField('Volume Weighted Average Price')
    adv_checkbox = BooleanField('Average Daily Volume')
    submit = SubmitField('Graph')
