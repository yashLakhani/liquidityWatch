from app.modules.calculate.liquidity_watch import (calculate_daily_volatility,
                                                 calculate_volume_weighted_average_price,
                                                 calculate_average_daily_volume)


def calculate_metrics(dataframe, VWAP_selected, ADV_selected, selected_price_column, selected_volume_column):
    dataframe['Date'] = dataframe.index.to_series()
    dataframe['Volatility'] = calculate_daily_volatility(dataframe, selected_price_column)

    if VWAP_selected and selected_price_column:
            dataframe['VWAP'] = calculate_volume_weighted_average_price(dataframe, selected_price_column)

    if ADV_selected and selected_volume_column:
            dataframe['ADV'] = calculate_average_daily_volume(dataframe, selected_volume_column)

    return dataframe