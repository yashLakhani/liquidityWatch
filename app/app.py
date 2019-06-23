from flask import render_template, redirect, request

from models import app
from forms import InstrumentSelectionForm
from graph import (bokeh_version,
                   create_line_graph,
                   create_candle_stick_graph,
                   generate_volatility_graph,
                   generate_price_graph,
                   generate_volume_graph)
from queries import (get_instrument_name,
                     get_instrument_details,
                     split_instrument_code)
from quandl_provider import (get_best_column,
                             fetch_market_data)
from metric_calculator import calculate_metrics

app.secret_key = 'XOYO!'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['DEBUG'] = True
app.vars = {}


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def instrument_selection():
    form = InstrumentSelectionForm()
    if request.method == 'GET':
        return render_template("index.html", form=form)
    else:
        populate_form_data(form)
        return redirect('/graph')


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    df = fetch_market_data(app.vars)
    selected_price_column = get_best_column('Price', df.columns)
    selected_volume_column = get_best_column('Volume', df.columns)
    price_col_to_plot = [selected_price_column]
    volume_col_to_plot = [selected_volume_column]

    df = calculate_metrics(df, app.vars['plotVWAP'],  app.vars['plotADV'],
                            selected_price_column, selected_volume_column)

    if 'VWAP' in df.columns:
        price_col_to_plot += ['VWAP']

    if 'ADV' in df.columns:
        volume_col_to_plot += ['ADV']

    bk_mc_price_script, bk_mc_price_div = generate_price_graph(df, selected_price_column,
                                                               price_col_to_plot,
                                                               plotVWAP=app.vars['plotVWAP'])
    bk_mc_volatility_script, bk_mc_volatility_div = generate_volatility_graph(df, selected_price_column,
                                                                              price_col_to_plot)
    bk_mc_volume_script, bk_mc_volume_div = generate_volume_graph(df, selected_volume_column,
                                                                  volume_col_to_plot,
                                                                  plotADV=app.vars['plotADV'])

    ins_name, ins_contract = get_instrument_details(app.vars['instrumentName'])

    return render_template('graph.html', ins_name=ins_name,
                           ins_contract=ins_contract, bv=bokeh_version,
                           price_script=bk_mc_price_script, price_div=bk_mc_price_div,
                           volume_script=bk_mc_volume_script, volume_div=bk_mc_volume_div,
                           vol_script=bk_mc_volatility_script, vol_div=bk_mc_volatility_div)


@app.errorhandler(500)
def error_handler(e):
    return render_template('error.html', ticker=app.vars['instrumentCode'])


def populate_form_data(form):
    app.vars['startDt'] = form.start_dt.data
    app.vars['endDt'] = form.end_dt.data
    app.vars['instrumentCode'] = form.instrument.data
    app.vars['instrumentName'] = get_instrument_name(split_instrument_code(app.vars['instrumentCode'])).name
    app.vars['plotVWAP'] = form.vwap_checkbox.data
    app.vars['plotADV'] = form.adv_checkbox.data


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)
