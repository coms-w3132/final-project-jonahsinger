"""
This class contains the backtester methods for the three strategies:
1. Linear Regression
2. Mean Reversion
3. Neural Network -- Incomplete

These strategies can be run and the parameters can be modified in the files:
LinearRegression.py
MeanReversion.py
NeuralNetwork.py
"""

import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt


class Backtester:
    def __init__(self, tickers, start_date, end_date, amount):
        self.tickers = tickers  # Stock symbols
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.amount = amount  # Starting money
        self.data = self.get_stock_data()  # Getting price data
        self.portfolio_value = self.amount
        self.previous_slopes = {}
        self.previous_mean_deviation = {}

    def get_stock_data(self):
        """Gets data for the specified tickers in the date range."""
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
        return data['Close'].dropna(how='all')  # drops null data

    def run_strategy(self, step_size, strategy):
        """Executes the trading strategy over defined periods."""
        trading_days = self.data.index
        start_idx = 0

        value_history = [(trading_days[start_idx], self.portfolio_value)]

        while start_idx < len(trading_days):
            end_idx = min(start_idx + step_size, len(trading_days) - 1)
            start_time, end_time = trading_days[start_idx], trading_days[end_idx]

            if start_idx > 0:  # Skip trading in the first period
                if (strategy == "linear regression") or (strategy == "reverse linear regression"):
                    current_value, investments = self.perform_step(start_time, end_time, self.previous_slopes)
                elif (strategy == "mean reversion") or (strategy == "reverse mean reversion"):
                    current_value, investments = self.perform_step(start_time, end_time, self.previous_mean_deviation)
                else:
                    current_value = 0
                """
                print(f"\nFrom {start_time.date()} to {end_time.date()}:")
                print("Trades executed:")
                for trade_type, orders in investments.items():
                    print(f"{trade_type.capitalize()}:")
                    for ticker, amount in orders.items():
                        print(f"  {ticker}: ${amount:.2f}")
                print(f"Return after this period: ${current_value - self.portfolio_value:.2f}")
                """
                self.portfolio_value = current_value
                value_history.append((end_time, self.portfolio_value))

            # Update slopes for the next period
            if strategy == "linear regression":
                self.previous_slopes = {ticker: self.do_linear_regression(ticker, start_time, end_time) for ticker in
                                        self.tickers}
            if strategy == "reverse linear regression":
                self.previous_slopes = {ticker: -self.do_linear_regression(ticker, start_time, end_time) for ticker in
                                        self.tickers}

            if strategy == "mean reversion":
                self.previous_mean_deviation = {ticker: self.calculate_mean_deviation(ticker, start_time, end_time)
                                                for ticker in self.tickers}

            start_idx = end_idx + 1

        self.plot_results(value_history)

    def perform_step(self, start_time, end_time, indicators):
        """Calculate buy and short orders based on previous period regression, then calculate returns."""
        if not indicators:  # No trading if there are no previous slopes (e.g., first period)
            return self.portfolio_value, {'buy': {}, 'short': {}}

        buy_orders, short_orders = self.allocate_funds(indicators)
        returns = self.calculate_returns(buy_orders, short_orders, start_time, end_time)
        return returns, {'buy': buy_orders, 'short': short_orders}

    def allocate_funds(self, indicators):
        """Allocate funds to buy and short stocks based on their slopes."""
        sorted_tickers = sorted(indicators, key=indicators.get, reverse=True)
        num_to_select = max(1, len(sorted_tickers) // 10)

        buy_tickers = sorted_tickers[:num_to_select]
        short_tickers = sorted_tickers[-num_to_select:]

        total_buy = sum(abs(indicators[t]) for t in buy_tickers)
        total_short = sum(abs(indicators[t]) for t in short_tickers)

        buy_orders = {t: (self.portfolio_value / 2) * (abs(indicators[t]) / total_buy) for t in buy_tickers}
        short_orders = {t: (self.portfolio_value / 2) * (abs(indicators[t]) / total_short) for t in short_tickers}

        return buy_orders, short_orders

    def calculate_returns(self, buy_orders, short_orders, start_time, end_time):
        """Calculate returns from buy and short positions based on actual price changes."""
        end_prices = self.data.loc[end_time]
        start_prices = self.data.loc[start_time]

        buy_return = sum((end_prices.get(ticker, 0) / start_prices.get(ticker, 1) - 1) * amount for ticker, amount in buy_orders.items())
        short_return = sum((1 - end_prices.get(ticker, 1) / start_prices.get(ticker, 0)) * amount for ticker, amount in short_orders.items())

        return self.portfolio_value + buy_return + short_return

    def do_linear_regression(self, ticker, start_time, end_time):
        """Perform linear regression on stock prices to return the slope."""
        prices = self.data[ticker].loc[start_time:end_time].dropna()
        if len(prices) < 2:
            return 0  # Not enough data points for a regression
        x = np.arange(len(prices)).reshape(-1, 1)
        y = prices.values
        model = LinearRegression()
        model.fit(x, y)
        return model.coef_[0]

    def calculate_mean_deviation(self, ticker, start_time, end_time):
        """Calculate the deviation from the mean for each ticker."""
        prices = self.data[ticker].loc[start_time:end_time].dropna()
        if prices.empty:
            return 0
        mean_price = prices.mean()
        return prices.iloc[-1] - mean_price  # Deviation from the mean

    def plot_results(self, value_history):
        """Plot the historical values of the portfolio over time."""
        dates, values = zip(*value_history)
        plt.figure(figsize=(10, 5))
        plt.plot(dates, values, 'o-')
        plt.title("Portfolio Value Over Time")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value ($)")
        plt.grid(True)
        plt.show()
