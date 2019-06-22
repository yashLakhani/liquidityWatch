from flask import render_template, redirect, request

from models import app
from forms import InstrumentSelectionForm
from graph import (bokeh_version,
                   create_line_graph,
                   create_candle_stick_graph,
                   initialise_empty_graphs)
from queries import (get_instrument_name,
                     get_instrument_details,
                     split_instrument_code)
from liquiditywatch import (get_best_column,
                           calculate_volume_weighted_average_price,
                           calculate_daily_volatility,
                           calculate_average_daily_volume)

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
        app.vars['start_dt'] = form.start_dt.data
        app.vars['end_dt'] = form.end_dt.data
        app.vars['ins_code'] = form.instrument.data
        app.vars['ins_name'] = get_instrument_name(split_instrument_code(app.vars['ins_code'])).name
        app.vars['VWAP_selected'] = form.vwap_checkbox.data
        app.vars['ADV_selected'] = form.adv_checkbox.data
        return redirect('/graph')


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    import quandl

    bk_mc_price_script, bk_mc_price_div = initialise_empty_graphs()
    bk_mc_volume_script, bk_mc_volume_div = initialise_empty_graphs()
    bk_mc_volatility_script, bk_mc_volatility_div = initialise_empty_graphs()

    if app.vars['ins_code']:
            df = quandl.get("CHRIS/{}".format(app.vars['ins_code']),
                    start_date=app.vars['start_dt'],
                    end_date=app.vars['end_dt'])

            selected_price_column = get_best_column('Price', df.columns)
            selected_volume_column = get_best_column('Volume', df.columns)
            price_columns_to_plot = [selected_price_column]
            volume_columns_to_plot = [selected_volume_column]

            df['Date'] = df.index.to_series()
            df['Volatility'] = calculate_daily_volatility(df, selected_price_column)

            if app.vars['VWAP_selected'] and selected_price_column:
                df['VWAP'] = calculate_volume_weighted_average_price(df, selected_price_column)
                price_columns_to_plot += ['VWAP']
            if app.vars['ADV_selected'] and selected_volume_column:
                df['ADV'] = calculate_average_daily_volume(df, selected_volume_column)
                volume_columns_to_plot += ['ADV']

            if selected_price_column:
                bk_mc_price_script, bk_mc_price_div = create_line_graph(df, price_columns_to_plot,
                                                                                   width=1000, height=400,
                                                                                   colors=['#FF7F50', '#A6CEE3'])
                bk_mc_volatility_script, bk_mc_volatility_div = create_line_graph(df, ['Volatility'],
                                                                                  width=1000, height=250,
                                                                                  colors=["limegreen"])

            if selected_volume_column:
                bk_mc_volume_script, bk_mc_volume_div = create_line_graph(df, volume_columns_to_plot,
                                                                         width=1000, height=250,
                                                                         colors=["grey", 'yellow'],
                                                                         format=True)

            ins_name, ins_contract = get_instrument_details(app.vars['ins_name'])

            return render_template('graph.html', ins_name=ins_name,
                                   ins_contract=ins_contract, bv=bokeh_version,
                                   price_script=bk_mc_price_script, price_div=bk_mc_price_div,
                                   volume_script=bk_mc_volume_script, volume_div=bk_mc_volume_div,
                                   vol_script=bk_mc_volatility_script, vol_div=bk_mc_volatility_div)

    return render_template('error.html', ticker=app.vars['ticker'], year=app.vars['start_year'])


@app.errorhandler(500)
def error_handler(e):
    return render_template('error.html', ticker=app.vars['ticker'], year=app.vars['start_year'])


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)
