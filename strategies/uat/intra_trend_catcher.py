import pandas as pd
import datetime as dt
from databases.paths import QuotesPath, UATResultsPath
from tools.misc.database_misc import get_from_db, generate_folder
from tools.misc.dates_misc import yesterday
from tools.strategies_toolbox.intra_vs_close import compare_close_open_one_day, compare_close_intra
from strategies.strategy_classes.signal import Signal

pd.options.mode.chained_assignment = None

"""
Look back last 20 min, if abs(perf) > 0.5%, enters the market for the next 40 min.
The objective is to catch an info release, whatever that is and it's impact, and follow the drift.

There are also calm period with no news where the market tends to slowly drift. The way it drifts correspond 
to the last tendency way, meaning if the last new has a negative impact and no news until then, it will negatively drift.
(especially during afternoons with lower volumes).
"""

interval_comparison_dict = {'daily': 'daily', 'intraday': 'intra_2m'}
way_dict = {
    'bullish': 'UCO',
    'bearish': 'SCO'
}
gain_interval = 0.017
threshold = -0.015
time_step_long_perf = 16
time_step_short_ave_perf = 3
stoplosslevel = 0.019
# global_floor = -0.022
global_floor = -0.5


def run_strat():
    etfs = [
        'UCO',
        # 'SCO'
    ]

    etf_dict, date_r = load_data(
        etfs=etfs,
        period=2052
    )
    # intra_dfs = enrich_data(
    #     intra_dfs=etf_dict,
    #     date_filter=date_r
    # )

    # Save
    # for etf, df in intra_dfs.items():
    #     df.to_csv(UATResultsPath + f'intra_trend_catcher_save_{etf}.csv')

    # Load
    intra_dfs = {}
    for etf in etfs:
        df = pd.read_csv(UATResultsPath + f'intra_trend_catcher_save_{etf}.csv', index_col='timestamp')
        # some columns types are reset
        df.index = pd.to_datetime(df.index, format='mixed')
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].map(lambda x: x.date())
        intra_dfs[etf] = df

    # Runs strat logic and gather pnl
    signals_list = []
    pnl_list = []
    pnl_arith = 0
    pnl_geom = 1
    raw_res_list = []
    analyzed_res_list = []
    for date in date_r:
        pnl, signals = apply_logic(
            intra_dfs,
            date
        )
        pnl_list.append(pnl)
        signals_list.append(signals)
        print(f"Done for {date.date()} with pnl : {pnl['pnl%']}")
        # if intra_df.empty:
        #     print('No data for ' + str(date.date()))
        # else:
        #     raw_res = process_results(
        #         intra_df
        #     )
        #
        #     analyzed_res = analyze_results(
        #         raw_res
        #     )
        #     raw_res_list.append(raw_res)
        #     analyzed_res_list.append(analyzed_res)
        #     print('Results computed for ' + str(date.date()))

    for pnl in pnl_list:
        pnl_arith += pnl['pnl%']
        print(f'Arithmetic PnL: {pnl_arith}')
    for pnl in pnl_list:
        pnl_geom = pnl_geom * (1+(pnl['pnl%']/100))
        print(f'Geometric PnL: {pnl_geom}')

    # aggregation of each date simu
    strat_raw_result = pd.concat(raw_res_list)
    strat_analyzed_result = pd.concat(analyzed_res_list)

    strat_raw_result.to_csv('strat_raw_result.csv')
    strat_analyzed_result.to_csv('strat_analyzed_result.csv')


def load_data(
        etfs,
        period
):
    """
    Loader
    """

    etf_data = {}

    # date
    date_range = pd.bdate_range(
        end=yesterday(dt.datetime.today()),
        periods=period,
        freq="C",
        # holidays=["2023-09-04", "2023-06-19", "2023-07-04"]
        holidays=[
            "2023-01-16",
            "2023-02-20",
            "2023-04-07",
            "2023-05-29",
            "2023-06-19",
            "2023-07-04",
            "2023-09-04",
            "2023-11-23"
        ]
        # holidays=[]
    )

    # for etf in etfs:
    #     etf_data[etf] = get_from_db(
    #         path=QuotesPath + etf + f'\\intra_2m_{etf}.csv',
    #         index_name='timestamp'
    #     )
    for etf in etfs:
        etf_data[etf] = get_from_db(
            path=QuotesPath + etf + f'\\UCO_2M_from_2016-01-01_to_2023-11-24_EST.csv',
            index_name='timestamp'
        )

    return etf_data, date_range


def enrich_data(
        intra_dfs,
        date_filter
):
    """
    Filters data with dates range.
    Computes intraday returns.
    """
    # Filter
    intra_dfs, filter_dates(
        intra_dfs,
        date_filter
    )


    # Intra returns
    intra_dfs_filled = {}
    dfs_to_concat = []
    for udl, intra_df in intra_dfs.items():
        intra_df = intra_df[['Close', 'ticker',  'date']]
        # Scrolls through each day and each time interval and enrich with formulas
        for date in intra_df['date'].unique().tolist():
            # We select the day we need to run the formulas on, and
            df = intra_df.loc[intra_df['date'] == date]

            # Fills new columns
            df['Return'] = 0
            df[f'(A) Rolling performance over average last {time_step_long_perf} time steps'] = 0
            df[f'(B) Rolling performance over average last {time_step_short_ave_perf} time steps'] = 0

            # Creating a column dict {name: indexer} because we're scrolling with iloc
            col_dict = {col_name: num for num, col_name in zip(range(len(list(df.columns))), list(df.columns))}

            for i in range(len(df))[:]:
                # Computing return with first close intraday and every close price
                df.iloc[i, col_dict['Return']] = ((df.iloc[i, col_dict['Close']] /
                                                   df.iloc[0, col_dict['Close']]) - 1) * 100

                # Indicator of long-term perf - averaged
                if i >= time_step_long_perf:
                    last_prices = [
                        df.iloc[price_index, col_dict['Close']]
                        for price_index in range(i - time_step_long_perf, i)
                    ]
                    average_last_prices = sum(last_prices) / time_step_long_perf
                    df.iloc[
                        i, col_dict[f'(A) Rolling performance over average last {time_step_long_perf} time steps']] = \
                        ((df.iloc[i, col_dict['Close']] / average_last_prices) - 1) * 100

                # Indicator of short-term per
                # - averaged
                if i >= time_step_long_perf:
                    last_prices = [
                        df.iloc[price_index, col_dict['Close']]
                        for price_index in range(i - time_step_short_ave_perf, i)
                    ]
                    average_last_prices = sum(last_prices) / time_step_short_ave_perf
                    df.iloc[i, col_dict[
                        f'(B) Rolling performance over average last {time_step_short_ave_perf} time steps']] = \
                        ((df.iloc[i, col_dict['Close']] / average_last_prices) - 1) * 100

            print(f"Done for {date}")
            dfs_to_concat.append(df)
        intra_dfs_filled[udl] = pd.concat(dfs_to_concat)

    return intra_dfs_filled


def apply_logic(
        intra_dfs,
        date
):
    """
    Generates signal
    """
    # We might as well only use UCO cause both UCO and SCO are symmetric, but in practice the short selling
    # will be materialized by a long SCO
    intra_df = intra_dfs['UCO']
    intra_df = intra_df.loc[intra_df['date'] == date.date()]

    # Signal/Position/Event/Pnl dicos/lists TODO creates class objects io dico
    signals_list = []
    position = {}
    position['amount'] = 0
    positions_list = []
    event = {}
    events_list = []
    pnl = {}
    pnl['pnl%'] = 0
    pnl_list = []

    # Indexing of columns in a dict, needed to use with iloc (only integers allowed)
    col_dict = {col_name: num for num, col_name in zip(range(len(list(intra_df.columns))), list(intra_df.columns))}

    # Find the 15:30 exit row index // Pas tres beau
    try:
        exittime_index = \
            [i for i, row in zip(range(len(intra_df.index)), intra_df.index) if row.hour == 15 and row.minute == 30][0]
        exittime_index = exittime_index + 2
    except:
        try:
            exittime_index = \
                [i for i, row in zip(range(len(intra_df.index)), intra_df.index) if row.hour == 15 and row.minute == 32][0]
            exittime_index = exittime_index + 2
        except:
            exittime_index = len(intra_df)

    # print(exittime_index)
    # scroll through minutes, starting with 20th constatation
    for i in range(len(intra_df))[time_step_long_perf + 10: exittime_index]:
        """
        We split the analysis in two : Is there a position booked already, or not ?
        Then we apply the following logics :
            - No position ? Is there a signal ? If yes we enter the market
            - Position ? If yes, is the stop loss hit ? Is it 15:30 ? Do we need to adjust the stop loss ? 
        """
        # TODO we could implement storage function within their classes to keep a registry of signal/event and a logger

        # Instanciation of Signal, and defaulting some params
        signal = Signal()
        signal.update({'order_type': "market_order", 'stoplosslevelreached_update': 1})

        # Signal dico
        # We truncate the intra_df, send it to signal computation, along with our position indications
        signal = compute_logic(
            signal=signal,
            df=intra_df.iloc[i - time_step_long_perf:i, :],
            position=position,
            pnl=pnl
        )

        # Event dico
        # Here a signal turns to an event, example: our signal was sent to the market and settled at certain price/time.
        # Since we're in UAT, we're considering we get executed to the next close price.
        # NB: the signal/event spreads needs to be stored in Prod and analyzed to improve execution
        if signal.signal_type is not None:
            signals_list.append(signal)  # if our signal is not just a timestamp
            # event = process_signal(signal)
            position, pnl = compute_position(signal, position, pnl)
            positions_list.append(position)
            pnl_list.append(pnl)

    return pnl, signals_list


def compute_logic(signal, df, position, pnl):
    """
    Compute signal logic, considering trend and time_decay parameters
    """
    close = df.iloc[time_step_long_perf - 1, :]['Close']
    signal.update({'timestamp': df.iloc[time_step_long_perf - 1, :].name})

    # Trend condition
    # list of booleans to check if last 10 returns observed are all positive or negative
    is_trend_list = list(
        df[f'(A) Rolling performance over average last {time_step_long_perf} time steps'].apply(
            lambda x: True if x > 0 else False)
    )
    ispostrend = all(is_trend_list)  # positive trend bool
    isnegtrend = not any(is_trend_list)  # negative trend bool
    is_no_trend = bool(ispostrend == isnegtrend)  # no trend

    if pnl['pnl%'] > global_floor:
        # Market entrance signal, after 11:00 to avoid morning swings
        if ispostrend and position['amount'] == 0 and bool(
            df.iloc[time_step_long_perf - 1, :].name.hour >= 11 and
            df.iloc[time_step_long_perf - 1, :].name.minute >= 00
        ):
            signal.update({'way': "buy", 'price': close, 'signal_type': "entry", "reason": "uptrend"})
        if isnegtrend and position['amount'] == 0 and bool(
            df.iloc[time_step_long_perf - 1, :].name.hour >= 11 and
            df.iloc[time_step_long_perf - 1, :].name.minute >= 00
        ):
            signal.update({'way': "sell", 'price': close, 'signal_type': "entry", "reason": "down_trend"})

    # Market exit signals
    # StopLoss condition
    if position['amount'] != 0 and position['way'] == 'long':
        # TODO here we go with Short and Long for the backtest but we're always long in the end (long SCO or UCO)
        islimithit = bool(close < position['stoplosslimitprice'])
        if islimithit:
            signal.update({'way': "sell", 'price': close, 'signal_type': "exit", "reason": "down&hit"})

    if position['amount'] != 0 and position['way'] == 'short':
        islimithit = bool(close > position['stoplosslimitprice'])
        if islimithit:
            signal.update({'way': "buy", 'price': close, 'signal_type': "exit", "reason": "up&hit"})

        # Time condition => Has the trade timed out ?
    istimedout = bool(
        df.iloc[time_step_long_perf - 1, :].name.hour == 15 and
        df.iloc[time_step_long_perf - 1, :].name.minute >= 30
    )
    if istimedout and position['amount'] != 0 and position['way'] == 'long':
        signal.update({'way': "sell", 'price': close, 'signal_type': "exit", "reason": "timed_out"})
    if istimedout and position['amount'] != 0 and position['way'] == 'short':
        signal.update({'way': "buy", 'price': close, 'signal_type': "exit", "reason": "time_out"})

    # StopLoss amendment
    # Moving StopLoss
    if position['amount'] != 0:
        if position['trend_way_entry'] == 'positive' and close > position['max_price']:
            signal.update({
                'max_price_update': close,
                'stoplosslimitprice_update': close * (1 - stoplosslevel),
                'signal_type': "stoplossmoving_amend",
                "reason": "stoploss_movingup"
            })

        if position['trend_way_entry'] == 'negative' and close < position['min_price']:
            signal.update({
                'min_price_update': close,
                'stoplosslimitprice_update': close * (1 + stoplosslevel),
                'signal_type': "stoplossmoving_amend",
                "reason": "stoploss_movingdown"
            })

    # Trend condition  => Has the trend reversed ?
    if position['amount'] != 0:
        # if bullish trend loses speed, we tighten our stoploss range
        if position['trend_way_entry'] == 'positive' and is_no_trend and position['stoplosslevelreached'] < 2:
            signal.update({
                'trend_way_update': 'none',
                'stoplosslimitprice_update': position['stoplosslimitprice'] / (1 - stoplosslevel) * (
                        1 - stoplosslevel * 1.20),
                'stoplosslevelreached_update': 2,
                'signal_type': "stoploss_amend",
                "reason": "trend_stopped"
            })
        # if bearish trend loses speed, we tighten our stoploss range
        if position['trend_way_entry'] == 'positive' and is_no_trend and position['stoplosslevelreached'] < 2:
            signal.update({
                'trend_way_update': 'none',
                'stoplosslimitprice_update': position['stoplosslimitprice'] / (1 + stoplosslevel) * (
                        1 + stoplosslevel * 1.20),
                'stoplosslevelreached_update': 2,
                'signal_type': "stoploss_amend",
                "reason": "trend_stopped"
            })

    # TODO Trend condition  => Did the trend come back ?

    # Time condition => Do we need to reduce our limit level to the time decay of our trade /
    if position['amount'] != 0:
        if position['trend_way_now'] == 'positive':
            # 2 hours since last signal
            if (position['timestamp'].hour - signal.timestamp.hour) > 2 and position['stoplosslevelreached'] < 2:
                signal.update({
                    'stoplosslimitprice_update': position['stoplosslimitprice'] / (1 - stoplosslevel) * (
                            1 - stoplosslevel * 1.20),
                    'stoplosslevelreached_update': 2,
                    'signal_type': "stoploss_amend",
                    "reason": "2hours"})
            # 3 hours since last signal
            if (position['timestamp'].hour - signal.timestamp.hour) > 3 and position['stoplosslevelreached'] < 3:
                signal.update({
                    'stoplosslimitprice_update': position['stoplosslimitprice'] / (1 - stoplosslevel * 1.20) * (
                            1 - stoplosslevel * 1.40),
                    'stoplosslevelreached_update': 3,
                    'signal_type': "stoploss_amend",
                    "reason": "3hours"})

        if position['trend_way_now'] == 'negative':
            if (position['timestamp'].hour - signal.timestamp.hour) > 2 and position['stoplosslevelreached'] < 2:
                signal.update({
                    'stoplosslimitprice_update': position['stoplosslimitprice'] / (1 + stoplosslevel) * (
                            1 + stoplosslevel * 1.20),
                    'stoplosslevelreached_update': 2,
                    'signal_type': "stoploss_amend",
                    "reason": "2hours"})

            if (position['timestamp'].hour - signal.timestamp.hour) > 3 and position['stoplosslevelreached'] < 3:
                signal.update({
                    'stoplosslimitprice_update': position['stoplosslimitprice'] / (1 + stoplosslevel * 1.20) * (
                            1 + stoplosslevel * 1.40),
                    'stoplosslevelreached_update': 3,
                    'signal_type': "stoploss_amend",
                    "reason": "3hours"})

    return signal


def process_signal(signal):
    # TODO when we move to prod
    """
    We execute the signal. Example: book a market order.
    We wait for the execution to take place or not.
    The response is our event.
    """
    event = {}
    # launch booking

    # request the platform

    # fill the event object with the exec price
    return event


def compute_position(signal, position, pnl):
    """
    Compute the position to track our pnl
    """
    # Set up
    position['timestamp'] = signal.timestamp
    pnl['timestamp'] = signal.timestamp

    # Orders
    if signal.signal_type == "entry":
        if signal.way == 'buy':
            position['way'] = 'long'
            position['amount'] = 1
            position['amount_change'] = +1
            position["previous_price"] = 0
            position['price'] = signal.price
            position['max_price'] = signal.price
            position['min_price'] = signal.price
            position['trend_way_entry'] = 'positive'
            position['trend_way_now'] = 'positive'
            position['stoplosslimitprice'] = signal.price * (1 - stoplosslevel)
            position['stoplosslevelreached'] = signal.stoplosslevelreached_update

        if signal.way == 'sell':
            position['way'] = 'short'
            position['amount'] = -1
            position['amount_change'] = -1
            position["previous_price"] = 0
            position['price'] = signal.price
            position['max_price'] = signal.price
            position['min_price'] = signal.price
            position['trend_way_entry'] = 'negative'
            position['trend_way_now'] = 'negative'
            position['stoplosslimitprice'] = signal.price * (1 + stoplosslevel)
            position['stoplosslevelreached'] = signal.stoplosslevelreached_update

    if signal.signal_type == "exit":
        if signal.way == 'buy':
            position['way'] = 'flat'
            position['amount'] = 0
            position['amount_change'] = +1
            position["previous_price"] = position['price']
            position['price'] = signal.price
            position['max_price'] = signal.price
            position['min_price'] = signal.price
            position['trend_way_entry'] = 'none'
            position['trend_way_now'] = 'none'
            position['stoplosslimitprice'] = 0
            position['stoplosslevelreached'] = 1
            pnl['pnl%'] += -100 * ((position['price'] - position["previous_price"]) / position["previous_price"])

        if signal.way == 'sell':
            position['way'] = 'flat'
            position['amount'] = 0
            position['amount_change'] = -1
            position["previous_price"] = position['price']
            position['price'] = signal.price
            position['max_price'] = signal.price
            position['min_price'] = signal.price
            position['trend_way_entry'] = 'none'
            position['trend_way_now'] = 'none'
            position['stoplosslimitprice'] = 0
            position['stoplosslevelreached'] = 1
            pnl['pnl%'] += 100 * ((position['price'] - position["previous_price"]) / position["previous_price"])

    # StopLoss amend
    if signal.signal_type == "stoplossmoving_amend":
        position['max_price'] = signal.max_price_update
        position['min_price'] = signal.min_price_update
        position['stoplosslimitprice'] = signal.stoplosslimitprice_update
    if signal.signal_type == "stoploss_amend":
        position['trend_way_now'] = signal.trend_way_update
        position['stoplosslimitprice'] = signal.stoplosslimitprice_update
        position['stoplosslevelreached'] = signal.stoplosslevelreached_update

    return position, pnl


def analyze_results(res):
    macro_results = {}

    # Results gathering
    macro_results['daily_return'] = sum(res.set_index('date')['daily_return'].unique().tolist())
    # macro_results['daily_vol'] = res['daily_vol'].unique()[0]
    macro_results['gain_interval'] = res['gain_interval'].unique()[0]
    macro_results['colle'] = sum([res.set_index('date')['colle'].to_dict().values()][0])
    daily_transaction_number_list = [res.set_index('date')['transaction_number'].to_dict().values()][0]
    macro_results['total_transaction_number'] = sum(daily_transaction_number_list)
    macro_results['average_transaction_number'] = \
        sum(daily_transaction_number_list) / len(daily_transaction_number_list)

    macro_results_df = pd.DataFrame.from_dict(macro_results, orient='index').T

    return macro_results_df


def filter_dates(
        intra_dfs,
        date_filter
):
    # index reworking to dt
    for intra_df in intra_dfs.values():
        intra_df.index = pd.to_datetime(intra_df.index, format='mixed')

    date_filter = [date.date() for date in date_filter]

    # restricts intra_df's date range to user date range
    # -----------------------------------------------
    # restriction
    intra_dfs_rwd = {}
    for udl, intra_df in intra_dfs.items():
        intra_df['date'] = intra_df.index.map(lambda x: x.date())
        intra_df = intra_df.loc[intra_df['date'].isin(date_filter)]
        intra_dfs_rwd[udl] = intra_df

    # restricts daily close to intra_df's date range
    # -----------------------------------------------
    intra_date_range = list(
        set([date.date() for date in list(intra_dfs.values())[0].index.to_list()])
    )

    # we add a previous BD to our analysis exple: intra 26/08 needs 25/08
    intra_date_range.sort()
    intra_date_range.append(yesterday(intra_date_range[0]))

    return intra_dfs_rwd, intra_date_range


if __name__ == '__main__':
    run_strat()