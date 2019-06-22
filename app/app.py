from flask import Flask, Response, render_template, redirect, request

from models import app
from forms import InstrumentSelectionForm, get_instrument_name
from graph import bokeh_version, create_single_line_graph, create_candle_stick_graph
from liquiditywatch import (get_best_column,
                           calculate_volume_weighted_average_price,
                           calculate_daily_volatility)

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
        app.vars['ins_name'] = get_instrument_name(app.vars['ins_code'].split('_')[1]).name
        return redirect('/graph')


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    import quandl

    if app.vars['ins_code']:
            df = quandl.get("CHRIS/{}".format(app.vars['ins_code']),
                    start_date=app.vars['start_dt'],
                    end_date=app.vars['end_dt'])

            df['Date'] = df.index.to_series()


            selected_column = get_best_column('Price', df.columns)
            #df = calculate_volume_weighted_average_price(df, selected_column)

            df['Volatility'] = calculate_daily_volatility(df, selected_column)
            #print(df.columns)
            require_col = ['High', 'Low', 'Open', 'Last']
            # if all(x in df.columns for x in require_col):
            #     #print('yes')
            #
            #     bk_mc_price_script, bk_mc_price_div = create_candle_stick_graph(df, width=1000, height=450)
            # else:
                #print('no')
            bk_mc_price_script, bk_mc_price_div = create_single_line_graph(df, selected_column,
                                                                               width=1000, height=400,
                                                                               color="red",
                                                                               legend='Price')

            selected_column = get_best_column('Volume', df.columns)
            bk_mc_volume_script, bk_mc_volume_div = create_single_line_graph(df, selected_column,
                                                                             width=1000, height=250,
                                                                             color="grey",
                                                                             legend='Volume')

            bk_mc_volatility_script, bk_mc_volatility_div = create_single_line_graph(df, 'Volatility',
                                                                             width=1000, height=250,
                                                                             color="green",
                                                                             legend='Volatility')

            ins_name, ins_contract = app.vars['ins_name'].split(',')

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
