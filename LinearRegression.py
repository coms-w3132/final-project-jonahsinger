import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import yfinance as yf


class LinearRegressionStrategy:
    def __init__(self, tickers, start_date, end_date, amount):
        """
        Initialize the strategy.

        :param tickers: list of stock ticker symbols
        :param start_date: string, start date for the data in 'YYYY-MM-DD' format
        :param end_date: string, end date for the data in 'YYYY-MM-DD' format
        :param amount: float, total amount of money to trade with
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.amount = amount
        self.data = self.download_data()

    def download_data(self):
        """
        Download historical stock data for given tickers and timeframe using yfinance.
        """
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
        return data['Close']  # We focus on closing prices

    def fit_linear_regression(self, prices):
        """
        Fit a linear regression model to the prices and return the slope.

        :param prices: numpy array of prices
        :return: slope of the regression line
        """
        model = LinearRegression()
        X = np.arange(len(prices)).reshape(-1, 1)  # Reshape data to fit model requirements
        model.fit(X, prices)
        slope = model.coef_[0]
        return slope

    def execute_strategy(self):
        """
        Perform linear regression, select top and bottom 10% stocks, and calculate buy and sell orders.

        :return: dict, containing buy and sell orders with amounts for each stock
        """
        slopes = {}
        for ticker in self.tickers:
            prices = self.data[ticker].dropna()  # Ensure there are no NaN values
            if len(prices) > 1:  # Need at least two data points to fit a line
                slope = self.fit_linear_regression(prices)
                slopes[ticker] = slope

        # Sort tickers based on the slope
        sorted_tickers = sorted(slopes, key=slopes.get)
        num_stocks = len(sorted_tickers)

        # Calculate top and bottom 10% indices
        top_10_percent_index = int(0.9 * num_stocks)
        bottom_10_percent_index = int(0.1 * num_stocks)

        # Select top 10% and bottom 10% stocks
        buy_stocks = sorted_tickers[top_10_percent_index:]
        short_stocks = sorted_tickers[:bottom_10_percent_index]

        # Allocate funds: half for buying and half for shorting
        buy_amount = self.amount * 0.5
        short_amount = self.amount * 0.5

        # Calculate investment proportion based on the absolute values of slopes
        buy_slopes_sum = sum(abs(slopes[ticker]) for ticker in buy_stocks)
        short_slopes_sum = sum(abs(slopes[ticker]) for ticker in short_stocks)

        buy_orders = {ticker: (abs(slopes[ticker]) / buy_slopes_sum) * buy_amount for ticker in buy_stocks}
        short_orders = {ticker: (abs(slopes[ticker]) / short_slopes_sum) * short_amount for ticker in short_stocks}

        return {
            'buy': buy_orders,
            'short': short_orders
        }

