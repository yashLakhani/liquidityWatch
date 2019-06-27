from app.models.instrument import Instrument


def summarize_instrument(instrument):
    instrument_name = instrument.name.split(',')[0]
    if len(instrument_name) > 50:
        instrument_name = instrument_name[:50]
    else:
        instrument_name = instrument_name

    instrument_summary = '{} ({})'.format(instrument_name, instrument.code)
    return instrument_summary


def get_all_instruments():
    instruments = Instrument.query.all()
    return [(i.exchange + '_' + i.code, summarize_instrument(i)) for i in instruments]


def get_instrument_name(code):
    return Instrument.query.filter_by(code=code).first()


def get_instrument_details(instrument_name):
    instrument_details = instrument_name.split(',')
    if len(instrument_details) == 2:
        ins_name, ins_contract = instrument_details
    else:
        ins_name = instrument_details[0]
        ins_contract = instrument_details[-1]

    return ins_name, ins_contract


def split_instrument_code(instrument_code):
    split_code = instrument_code.split('_')
    if len(split_code) > 1:
        return split_code[1]
    return split_code[0]