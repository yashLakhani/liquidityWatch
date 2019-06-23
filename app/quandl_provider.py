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


def fetch_market_data(quandl_specs):
    import quandl
    if quandl_specs['instrumentCode']:
        try:
            dataframe = quandl.get("CHRIS/{}".format(quandl_specs['instrumentCode']),
                        start_date=quandl_specs['startDt'],
                        end_date=quandl_specs['endDt'])
        except Exception as e:
            raise Exception("Failed to fetch market data", e)

    return dataframe
