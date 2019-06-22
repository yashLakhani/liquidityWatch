import numpy as np
import bokeh
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.themes import built_in_themes
from bokeh.io import curdoc

bokeh_version = bokeh.__version__


def create_single_line_graph(dataframe, selected_column, width, height, color, legend):
    tmpx = np.array([0])
    tmpy = np.array([0])
    if selected_column:
        tmpx = np.array([dataframe['Date'], dataframe['Date'][::-1]]).flatten()
        tmpy = np.array([dataframe[selected_column], dataframe[selected_column][::-1]]).flatten()

    curdoc().theme = 'dark_minimal'
    plot = figure(plot_width=width, plot_height=height, x_axis_type="datetime")
    plot.patch(tmpx, tmpy, alpha=0.3, color=color, legend=legend)
    bk_mc_script, bk_mc_div = components(plot)

    return bk_mc_script, bk_mc_div


def create_candle_stick_graph(dataframe, width, height):
    inc = dataframe['Last'] > dataframe['Open']
    dec = dataframe['Open'] > dataframe['Last']
    w = 12 * 60 * 60 * 1000  # half day in ms

    import math
    curdoc().theme = 'dark_minimal'
    plot = figure(plot_width=width, plot_height=height, x_axis_type="datetime")
    plot.xaxis.major_label_orientation = math.pi / 4
    plot.grid.grid_line_alpha = 0.3

    plot.segment(dataframe['Date'], dataframe['High'], dataframe['Date'], dataframe['Low'], color='black')
    plot.vbar(dataframe['Date'][inc], w, dataframe['Open'][inc], dataframe['Last'][inc],
              fill_color="#D5E1DD", line_color="black")
    plot.vbar(dataframe['Date'][dec], w, dataframe['Open'][dec], dataframe['Last'][dec],
              fill_color="#F2583E", line_color="black")

    bk_mc_script, bk_mc_div = components(plot)

    return bk_mc_script, bk_mc_div


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
'''
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
'''
# render graph template
# ------------------- ------------------------|
# script, div = components(p)