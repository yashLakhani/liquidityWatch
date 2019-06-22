from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.widgets import ListWidget, CheckboxInput
from models import Instrument


def get_all_instruments():
    instruments = Instrument.query.all()
    return [(i.exchange + '_' + i.code, i.name) for i in instruments]


def get_instrument_name(code):
    return Instrument.query.filter_by(code=code).first()


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class InstrumentSelectionForm(FlaskForm):
    start_dt = DateField('DatePicker', format='%Y-%m-%d')
    end_dt = DateField('DatePicker', format='%Y-m%-%d')
    instrument = SelectField(label='Instrument', choices=get_all_instruments())
    vwap_checkbox = BooleanField('Volume Weighted Average Price')
    adv_checkbox = BooleanField('Average Daily Volume')
    oi_checkbox = BooleanField('Intraday Open Interest')
    submit = SubmitField('Graph')
