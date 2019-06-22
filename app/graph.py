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


def initialise_empty_graphs():
    return '', ''


def create_line_graph(dataframe, selected_columns, width, height, colors, format=False):
    curdoc().theme = 'dark_minimal'
    plot = figure(plot_width=width, plot_height=height, x_axis_type="datetime")

    for color, column in zip(colors, selected_columns):

        if not column:
            tmpx = np.array([0])
            tmpy = np.array([0])

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