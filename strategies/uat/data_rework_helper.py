import pandas as pd
from datetime import datetime, timedelta
from tools.misc.database_misc import get_from_db
from databases.paths import AlpacaPath
from zoneinfo import ZoneInfo


def from_utc_to_timezone(date, timezone):
    """
    Takes a date list, finds the timestep to the chosen timezone, creates a dict
    with the mapping
    """
    new_date = date.astimezone(ZoneInfo(timezone))
    return new_date


def filter_for_market_open_trading_time(date):
    """
    Creates a list of booleans corresponding to the open market hours in the index of timestamps
    """
    # We can compare timestamps to datetime objects, so we transform the timestamp to datetime object
    # we compare them to the same day @ 9:30 and @16:00 to know if market is open

    ismarketopen = bool(
        datetime.fromtimestamp(datetime.timestamp(date)) > datetime(year=date.year, month=date.month, day=date.day,
                                                                    hour=9, minute=30) and \
        datetime.fromtimestamp(datetime.timestamp(date)) < datetime(year=date.year, month=date.month, day=date.day,
                                                                    hour=16, minute=0)
    )

    return ismarketopen


def filter_for_even_minutes(date):
    """
    We filter for a 2m intra df
    """
    isevenminute = bool(date.minute % 2 == 0)

    return isevenminute


if __name__ == '__main__':
    etf = 'SCO'
    df = get_from_db(
        path=AlpacaPath + etf + f'\\SCO_1M_from_2016-01-04_to_2023-11-24.csv',
        index_name='timestamp'
    )
    df.index = pd.to_datetime(df.index, format='mixed')
    index_tz_mapping = df.index.to_series().apply(func=from_utc_to_timezone, args=('US/Eastern',))
    df.index = df.index.map(index_tz_mapping)
    index_hour_range_mapping = df.index.to_series().apply(filter_for_market_open_trading_time)

    df["ismarketopen"] = df.index.map(index_hour_range_mapping)
    df = df.loc[df["ismarketopen"] == True,]
    index_minute_even_mapping = df.index.to_series().apply(filter_for_even_minutes)
    df["isevenminute"] = df.index.map(index_minute_even_mapping)
    df = df.loc[df["isevenminute"] == True,]

    df.to_csv(AlpacaPath + etf + f'\\SCO_2M_from_2016-01-01_to_2023-11-24_EST.csv')
    print('')
