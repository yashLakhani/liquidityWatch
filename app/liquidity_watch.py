import numpy as np


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
