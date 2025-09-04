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
bnd_historical = read_csv("datasets/bnd_historical.csv")
fed_historical = read_csv("datasets/fed_historical.csv")


def _transform_date(string, separator, format="MM-DD-YYYY"):
    if format == "YYYY-MM-DD":
        array = string.split(separator)
        return date(int(array[0]), int(array[1]), int(array[2]))

    array = string.split(separator)
    return date(int(array[2]), int(array[0]), int(array[1]))


def _transform_etf_historical(data):
    data["Date"] = data["Date"].apply(lambda x: _transform_date(x, "/"))
    data["Close/Last"] = data["Close/Last"].apply(
        lambda x: Decimal(x).quantize(Decimal("0.01"))
    )
    data.drop(columns=["Open", "High", "Low", "Volume"], inplace=True)
    return data


def _transform_fed_historical(data):
    data["observation_date"] = data["observation_date"].apply(
        lambda x: _transform_date(x, "-", "YYYY-MM-DD")
    )
    return data


def _normalize(data):
    df = pd.DataFrame(data)
    max = df.max()
    min = df.min()
    normalized = (df - min) / (max - min)
    return normalized


def get_chart_data():
    fed = _transform_fed_historical(fed_historical)
    lqd = _transform_etf_historical(lqd_historical)
    bnd = _transform_etf_historical(bnd_historical)

    df = pd.merge(left=fed, left_on="observation_date", right=lqd, right_on="Date")
    df.drop(columns=["Date"], inplace=True)
    df.rename(columns={"Close/Last": "lqd_prices"}, inplace=True)

    df = pd.merge(left=df, left_on="observation_date", right=bnd, right_on="Date")
    df.drop(columns=["Date"], inplace=True)
    df.rename(columns={"Close/Last": "bnd_prices"}, inplace=True)

    return df


def build_chart(df):

    x = df["observation_date"]
    y1, y2, y3 = (
        _normalize(df["FEDFUNDS"]),
        _normalize(df["lqd_prices"]),
        _normalize(df["bnd_prices"]),
    )
    plt.plot(x, y1, label="FEDFUNDS")
    plt.plot(x, y2, label="LQD")
    plt.plot(x, y3, label="BND")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.1), ncols=3)
    plt.show()


df = get_chart_data()
build_chart(df)
