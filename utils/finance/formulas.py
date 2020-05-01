import typing
import numpy as np
import pandas as pd

from utils.data.stock_price_data import get_stock_data, get_stocks_data
from utils.data.column_headings import CLOSE, RETURNS, ADJUSTED_CLOSING_PRICE
from utils.data.sample_rates import WEEK, MONTH
from utils.finance.constants import *


def calculate_volume_weighed_average_price(closing_prices: list, volumes: list) -> int:
    """
    Calculate VWAP using sum of daily_volume x price divided by total volume

    :param closing_prices: stock prices closing prices
    :type closing_prices: list
    :param volumes: stock volumes on those days
    :type volumes: list
    :return: VWAP prices
    :rtype: int
    """
    return np.sum(np.multiply(closing_prices, volumes))/np.sum(volumes)


def calculate_percentage_change(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate percentage change base on closing price

    :param data: stock data
    :type data: pd.Dataframe
    :return: percentage change
    :rtype: pd.Dataframe
    """
    return data[CLOSE].pct_change()


def calculate_returns_daily(code: str) -> pd.DataFrame:
    """
    Calculate daily returns given a code

    :param code: code of the company
    :type code: str
    :return: daily percentage change
    :rtype: pd.Dataframe
    """
    data = get_stock_data(code)
    return calculate_percentage_change(data)


def calculate_returns_weekly(code: str) -> pd.DataFrame:
    """
    Calculate weekly returns given a code

    :param code: code of the company
    :type code: str
    :return: weekly percentage change
    :rtype: pd.Dataframe
    """
    data = get_stock_data(code)
    data[CLOSE].resample(WEEK).ffill().pct_change()


def calculate_returns_monthly(code: str) -> pd.DataFrame:
    """
    Calculate monthly return given a code

    :param code: code of the company
    :type code: str
    :return: monthly percentage change
    :rtype: pd.Dataframe
    """
    data = get_stock_data(code)
    return data[CLOSE].resample(MONTH).ffill().pct_change()


def calculate_cumulative_returns(code: str) -> pd.DataFrame:
    """

    :param code: code of the company
    :type code: str
    :return: cumulative returns
    :rtype: pd.Dataframe
    """
    data = get_stock_data(code)
    data[RETURNS] = calculate_percentage_change(data)
    return (data[RETURNS] + 1).cumprod()


def calculate_volatility(code: str, rolling_window: int) -> pd.DataFrame:
    """

    :param code: code of the company
    :type code: str
    :param rolling_window: period of the window
    :type rolling_window: int
    :return: volatility
    :rtype: pd.Dataframe
    """
    data = get_stock_data(code)
    return calculate_percentage_change(data).rolling(rolling_window).std()


def calculate_annualised_volatility_for_daily_data(code: str, rolling_window: int) -> pd.DataFrame:
    """
    Annualised volatility for daily data

    :param code: code of the company
    :type code: str
    :param rolling_window: period of the window
    :type rolling_window: int
    :return: volatility
    :rtype: pd.Dataframe
    """
    return calculate_volatility(code, rolling_window)*np.sqrt(TRADING_DAYS_IN_A_YEAR)


def calculate_annualised_volatility_for_hourly_data(code: str, rolling_window: int) -> pd.DataFrame:
    """
    Annualised volatility for hourly data

    :param code: code of the company
    :type code: str
    :param rolling_window: period of the window
    :type rolling_window: int
    :return: volatility
    :rtype: pd.Dataframe
    """
    return calculate_volatility(code, rolling_window).np.sqrt(NUMBER_OF_TRADING_HOURS_A_DAY * TRADING_DAYS_IN_A_YEAR)


def calculate_percentage_change_based_on_adjusted_closing_price(code: str) -> pd.DataFrame:
    """
    Calculate percentage change of a company given a company code

    :param code: company code
    :type code: str
    :return: percentage changes
    :rtype: pd.Dataframe
    """
    return get_stock_data(code)[ADJUSTED_CLOSING_PRICE].pct_change()


def calculate_percentage_changes_based_on_adjusted_closing_price(codes: typing.List[str]) -> pd.DataFrame:
    """
    Calculate percentage change of a company given a company code

    :param codes: company codes
    :type codes: list[str]
    :return: percentage changes
    :rtype: pd.Dataframe
    """
    return get_stocks_data(codes)[ADJUSTED_CLOSING_PRICE].pct_change()


def calculate_correlation(codes: typing.List[str]):
    """
    Calculate the correlation between the given companies

    :param codes: list of company codes
    :type codes: List[str]
    :return: correlation matrix
    :rtype: pd.Dataframe
    """
    return calculate_percentage_changes_based_on_adjusted_closing_price(codes).dropna().corr()
