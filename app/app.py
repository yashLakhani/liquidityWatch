from flask import Flask, Response, render_template, redirect, request

from datamodels import app
from inputforms import InstrumentSelectionForm
from bokehgraph import bokeh_version, create_single_line_graph
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
        app.vars['instrument'] = form.instrument.data
        return redirect('/graph')


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    import quandl


    df = quandl.get("CHRIS/{}".format(app.vars['instrument']),
                    start_date=app.vars['start_dt'],
                    end_date=app.vars['end_dt'])

    df['Date'] = df.index.to_series()

    print(df)
    selected_column = get_best_column('Price', df.columns)
    df = calculate_volume_weighted_average_price(df, selected_column)

    print(df)
    print(selected_column)
    bk_mc_price_script, bk_mc_price_div = create_single_line_graph(df, selected_column,
                                                                   width=1000, height=450,
                                                                   color="red",
                                                                   legend='Price')

    selected_column = get_best_column('Volume', df.columns)
    bk_mc_volume_script, bk_mc_volume_div = create_single_line_graph(df, selected_column,
                                                                     width=1000, height=250,
                                                                     color="blue",
                                                                     legend='Volume')

    return render_template('graph.html', ticker=app.vars['instrument'], bv=bokeh_version,
                           price_script=bk_mc_price_script, price_div=bk_mc_price_div,
                           vol_script=bk_mc_volume_script, vol_div=bk_mc_volume_div)

    #return render_template('error.html', ticker=app.vars['ticker'], year=app.vars['start_year'])


@app.errorhandler(500)
def error_handler(e):
    return render_template('error.html', ticker=app.vars['ticker'], year=app.vars['start_year'])


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)
