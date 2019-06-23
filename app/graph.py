import numpy as np
import bokeh
import random
import math
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
from bokeh.models import NumeralTickFormatter

bokeh_version = bokeh.__version__


def create_empty_graphs():
    return '', ''


def create_line_graph(dataframe, width, height, colors, selected_columns, plotVWAP=False, plotADV=False, format=False):
    curdoc().theme = 'dark_minimal'
    plot = figure(plot_width=width, plot_height=height, x_axis_type="datetime")

    if plotVWAP:
        selected_columns += ['VWAP']
    if plotADV:
        selected_columns += ['ADV']

    for color, column in zip(colors, selected_columns):

        tmpx = np.array([dataframe['Date'], dataframe['Date'][::-1]]).flatten()
        tmpy = np.array([dataframe[column], dataframe[column][::-1]]).flatten()

        plot.line(tmpx, tmpy, color=color, legend=column)
        if format:
            plot.yaxis.formatter = NumeralTickFormatter(format="0")

    bk_mc_script, bk_mc_div = components(plot)

    return bk_mc_script, bk_mc_div


def create_candle_stick_graph(dataframe, width, height):
    inc = dataframe['Last'] > dataframe['Open']
    dec = dataframe['Open'] > dataframe['Last']
    w = 12 * 60 * 60 * 1000  # half day in ms

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


def generate_volatility_graph(dataframe, selected_price_column, selected_columns):
    if selected_price_column:
        return create_line_graph(dataframe, width=1000, height=250, colors=["limegreen"],
                                 selected_columns=['Volatility'])
    return create_empty_graphs()


def generate_price_graph(dataframe, selected_price_column, selected_columns, plotVWAP):
    if selected_price_column:
        return create_line_graph(dataframe, width=1000, height=400,
                                 colors=['orange', 'skyblue'], selected_columns=selected_columns,
                                 plotVWAP=plotVWAP)
    return create_empty_graphs()


def generate_volume_graph(dataframe, selected_volume_column, selected_columns, plotADV):
    if selected_volume_column:
        return create_line_graph(dataframe, width=1000, height=250, colors=["grey", 'yellow'],
                                 selected_columns=selected_columns, plotADV=plotADV, format=True)
    return create_empty_graphs()
