from flask import Flask, Response, render_template, redirect, request
import requests
import pandas as pd
import numpy as np


from instance.config import DB_URL

import bokeh
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.embed import components

bv = bokeh.__version__

from flask_wtf import Form
from wtforms import widgets, StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.widgets import ListWidget, CheckboxInput

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import app, Instrument

app.secret_key = 'SHH!'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['DEBUG'] = True
app.vars = {}
feat = ['Open', 'Close', 'Range']


def get_all_instruments():
    instruments = Instrument.query.all()
    return [(i.exchange + '_' + i.code, i.name) for i in instruments]


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class InstrumentSelectionForm(Form):
    start_dt = DateField('DatePicker', format='%Y-%m-%d')
    end_dt = DateField('DatePicker', format='%Y-m%-%d')
    instrument = SelectField(label='Instrument', choices=get_all_instruments())
    vwap_checkbox = BooleanField('Volume Weighted Average Price')
    adv_checkbox = BooleanField('Average Daily Volume')
    oi_checkbox = BooleanField('Intraday Open Interest')
    submit = SubmitField('Graph')


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


'''
@app.route('/index', methods=['GET', 'POST'])
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # request was a POST
        app.vars['ticker'] = request.form['ticker'].upper()
        app.vars['start_year'] = request.form['year']
        try:
            int(app.vars['start_year'])
            app.vars['tag'] = 'Start year specified as %s' % app.vars['start_year']
        except ValueError:
            app.vars['start_year'] = ''
            app.vars['tag'] = 'Start year not specified/recognized'
        app.vars['select'] = [feat[q] for q in range(3) if feat[q] in request.form.values()]
        return redirect('/graph')
    '''

from flask import jsonify
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = 'Butter'
    #search = request.args.get('q')
    some_engine = create_engine(DB_URL)

    # create a configured "Session" class
    Session = sessionmaker(bind=some_engine)

    # create a Session
    session = Session()
    q = session.query(Instrument).filter(Instrument.name.contains(search))
    print(q.all())
    results = [(mv.code, mv.name) for mv in q.all()]
    print(q.all())
    return jsonify(matching_results=results)




def intersection(heirarchy, df_columns):
    # Preserve List Order
    common = sorted(set(df_columns).intersection(heirarchy), key=lambda x: heirarchy.index(x))
    return common




def get_best_column(column_to_find, search_columns):
    # Columns returned by Quandl are unpredictable hence we must find a best match
    column_mapping = {"Price": ["Settle", "Previous Settlement", "Last", "Open", "High", "Low"],
                      "Open Interest": ["Open Interest", "Previous Day Open Interest"],
                      "Volume": ["Volume"]}

    selected_columns =  intersection(column_mapping[column_to_find], search_columns)

    if len(selected_columns) > 0:
        return selected_columns[0]

    else:
        return None

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    # Request data from Quandl and get into pandas
    # --------------------------------------------|

    import quandl

    df = quandl.get("CHRIS/{}".format(app.vars['instrument']),
                    start_date=app.vars['start_dt'],
                    end_date=app.vars['end_dt'])

    df['Date'] = df.index.to_series()
    selected_column = get_best_column('Price', df.columns)
    print(selected_column)
    if selected_column:
        p = figure(plot_width=450, plot_height=450, title=app.vars['instrument'], x_axis_type="datetime")
        tmpx = np.array([df.Date, df.Date[::-1]]).flatten()
        tmpy = np.array([df[selected_column], df[selected_column][::-1]]).flatten()
        p.patch(tmpx, tmpy, alpha=0.3, color="gray", legend='Range (High/Low)')

    else:
        raise ValueError('No Appropriate Columns Found')
    '''    
    req = 'https://www.quandl.com/api/v3/datasets/CHRIS/'
    req = '%s%s.json?&collapse=weekly' % (req, app.vars['instrument'])
    if not app.vars['start_dt'] == '':
        req = '%s&start_date=%s' % (req, app.vars['start_dt'])
    r = requests.get(req)
    cols = r.json()['dataset']['column_names'][0:5]
    df = pd.DataFrame(np.array(r.json()['dataset']['data'])[:, 0:5], columns=cols)
    df.Date = pd.to_datetime(df.Date)
    df[['Price']] = df[['Previous Settlement']].astype(float)
    print(df)
    #df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(float)
    # if not app.vars['start_year'] == '':
    # if df.Date.iloc[-1].year > int(app.vars['start_year']):
    # app.vars['tag'] = '%s, but Quandl record begins in %s' % (app.vars['tag'], df.Date.iloc[-1].year)
    # app.vars['desc'] = r.json()['dataset']['name'].split(',')[0]

    # Make Bokeh plot and insert using components
    # ------------------- ------------------------|
    p = figure(plot_width=450, plot_height=450, title=app.vars['instrument'], x_axis_type="datetime")
    tmpx = np.array([df.Date, df.Date[::-1]]).flatten()
    tmpy = np.array([df.Price, df.Price[::-1]]).flatten()
    p.patch(tmpx, tmpy, alpha=0.3, color="gray", legend='Range (High/Low)')
    '''
    '''
    if 'Range' in app.vars['select']:

    if 'Open' in app.vars['select']:
        p.line(df.Date, df.Open, line_width=2, legend='Opening price')
    if 'Close' in app.vars['select']:
        p.line(df.Date, df.Close, line_width=2, line_color="#FB8072", legend='Closing price')
    #p.legend.orientation = "top_left"
    '''
    # axis labels
    p.xaxis.axis_label = "Date"
    p.xaxis.axis_label_text_font_style = 'bold'
    p.xaxis.axis_label_text_font_size = '16pt'
    p.xaxis.major_label_orientation = np.pi / 4
    p.xaxis.major_label_text_font_size = '14pt'
    p.xaxis.bounds = (df.Date.iloc[-1], df.Date.iloc[0])
    p.yaxis.axis_label = "Price ($)"
    p.yaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '16pt'
    p.yaxis.major_label_text_font_size = '12pt'

    # render graph template
    # ------------------- ------------------------|
    script, div = components(p)
    #                           ttag=app.vars['desc'], yrtag=app.vars['tag'],
    return render_template('graph.html', bv=bv, ticker=app.vars['instrument'],
                           script=script, div=div)


@app.errorhandler(500)
def error_handler(e):
    return render_template('error.html', ticker=app.vars['ticker'], year=app.vars['start_year'])


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)
