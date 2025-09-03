from datetime import date
from decimal import Decimal

import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt


"""
Data Sources:
federal reserver bank: https://fred.stlouisfed.org/series/FEDFUNDS
lqd nasdaq: https://www.nasdaq.com/market-activity/etf/lqd/historical
"""

lqd_historical = read_csv("datasets/lqd_historical.csv")
fed_historical = read_csv("datasets/fed_historical.csv")


def _transform_date(string, separator, format="MM-DD-YYYY"):
    if format == "YYYY-MM-DD":
        array = string.split(separator)
        return date(int(array[0]), int(array[1]), int(array[2]))

    array = string.split(separator)
    return date(int(array[2]), int(array[0]), int(array[1]))


def get_lqd_historical():
    lqd_historical["Date"] = lqd_historical["Date"].apply(
        lambda x: _transform_date(x, "/")
    )
    lqd_historical["Close/Last"] = lqd_historical["Close/Last"].apply(
        lambda x: Decimal(x).quantize(Decimal("0.01"))
    )
    lqd_historical.drop(columns=["Open", "High", "Low", "Volume"], inplace=True)
    return lqd_historical


def get_fed_historical():
    fed_historical["observation_date"] = fed_historical["observation_date"].apply(
        lambda x: _transform_date(x, "-", "YYYY-MM-DD")
    )
    return fed_historical


def _normalize(data):
    df = pd.DataFrame(data)
    max = df.max()
    min = df.min()
    normalized = (df - min) / (max - min)
    return normalized


def get_chart_data():
    fed = get_fed_historical()
    lqd = get_lqd_historical()

    fed_rates_list = []
    dates_list = []
    lqd_prices_list = []

    for index, obj in fed_historical.iterrows():
        year = obj["observation_date"].year
        month = obj["observation_date"].month

        for index, row in lqd_historical.iterrows():
            if obj["observation_date"] in dates_list:
                break

            if row["Date"].year == year and row["Date"].month == month:
                fed_rates_list.append(obj["FEDFUNDS"])
                dates_list.append(obj["observation_date"])
                lqd_prices_list.append(row["Close/Last"])

    x = dates_list
    y1, y2 = _normalize(fed_rates_list), _normalize(lqd_prices_list)
    plt.plot(x, y1, label="FEDFUNDS")
    plt.plot(x, y2, label="LQD")
    plt.legend(loc="upper center",  bbox_to_anchor=(0.5, 1.1), ncols=2)
    # fig, axs = plt.subplots(2)
    # fig.suptitle('Vertically stacked subplots')
    # axs[0].plot(dates_list, lqd_prices_list)
    # axs[1].plot(dates_list, fed_rates_list)
    plt.show()


get_chart_data()
