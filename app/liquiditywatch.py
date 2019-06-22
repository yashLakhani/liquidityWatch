import numpy as np


def intersection(heirarchy, df_columns):
    # Preserve List Order
    common = sorted(set(df_columns).intersection(heirarchy), key=lambda x: heirarchy.index(x))
    return common


def get_best_column(column_to_find, search_columns):
    # Columns returned by Quandl are unpredictable hence we must find a best match
    column_mapping = {"Price": ["Settle", "Previous Settlement", "Last", "Open", "High", "Low"],
                      "Open Interest": ["Open Interest", "Previous Day Open Interest"],
                      "Volume": ["Volume"]}

    selected_columns = intersection(column_mapping[column_to_find], search_columns)

    if len(selected_columns) > 0:
        return selected_columns[0]

    else:
        return ''


def calculate_volume_weighted_average_price(dataframe, price_column):
    if 'Volume' in dataframe.columns:
        return (dataframe['Volume'] * dataframe[price_column]).cumsum() / dataframe['Volume'].cumsum()

    return None


def calculate_daily_volatility(dataframe, price_column, min_periods=20):
    daily_pct_change = dataframe[price_column].pct_change()
    daily_volatility = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)

    return daily_volatility


def calculate_average_daily_volume(dataframe, volume_column, window=200):
    if volume_column:
        return dataframe[volume_column].rolling(window).mean().shift(1)

    return None
