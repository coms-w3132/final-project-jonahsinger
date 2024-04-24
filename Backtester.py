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
import heapq

class Backtester:
    def __init__(self, tickers, start_date, end_date, amount):
        self.tickers = tickers  # Stock symbols
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.amount = amount  # Starting money
        self.data = self.get_stock_data()  # Getting price data
        self.portfolio_value = self.amount
        self.previous_slopes = {}
        self.previous_mean_deviations = {}

    def get_stock_data(self):
        """Gets data for the specified tickers in the date range from yfinance"""
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
        print(data['Close'].dropna(how='all'))
        return data['Close'].dropna(how='all')  # drops null data

    def run_strategy(self, step_size, strategy):
        """Executes the trading strategy over defined period."""
        trading_days = self.data.index
        start_idx = 0
        value_history = [(trading_days[start_idx], self.portfolio_value)]

        # Loops until the end of trading days
        while start_idx < len(trading_days):
            # Calculates start_time and end_time for the current step
            end_idx = min(start_idx + step_size, len(trading_days) - 1)
            start_time, end_time = trading_days[start_idx], trading_days[end_idx]

            if start_idx > 0:  # No trades are placed on first step because there is no prior data
                # Call preform step function with proper previous indicators
                if (strategy == "linear regression") or (strategy == "reverse linear regression"):
                    current_value, investments = self.perform_step(start_time, end_time, self.previous_slopes)
                elif (strategy == "mean reversion") or (strategy == "reverse mean reversion"):
                    current_value, investments = self.perform_step(start_time, end_time, self.previous_mean_deviations)
                else:
                    current_value = 0
                    investments = 0

                # Print all trades and their returns
                print(f"\nFrom {start_time.date()} to {end_time.date()}:")
                print("Trades executed:")
                for trade_type, orders in investments.items():
                    print(f"{trade_type.capitalize()}:")
                    for ticker, amount in orders.items():
                        print(f"  {ticker}: ${amount:.2f}")
                print(f"Return after this period: ${current_value - self.portfolio_value:.2f}")

                self.portfolio_value = current_value
                value_history.append((end_time, self.portfolio_value))

            # Update indicators for the next period
            if strategy == "linear regression":
                self.previous_slopes = {}
                for ticker in self.tickers:
                    self.previous_slopes[ticker] = self.do_linear_regression(ticker, start_time, end_time)

            if strategy == "reverse linear regression":
                self.previous_slopes = {}
                for ticker in self.tickers:
                    self.previous_slopes[ticker] = -self.do_linear_regression(ticker, start_time, end_time)

            if strategy == "mean reversion":
                self.previous_mean_deviations = {}
                for ticker in self.tickers:
                    self.previous_mean_deviations[ticker] = self.mean_deviation_indicator(ticker, start_time, end_time)

            if strategy == "reverse mean reversion":
                self.previous_mean_deviations = {}
                for ticker in self.tickers:
                    self.previous_mean_deviations[ticker] = -self.mean_deviation_indicator(ticker, start_time, end_time)

            start_idx = end_idx + 1

        self.plot_results(value_history)

    def perform_step(self, start_time, end_time, indicators):
        """Calculate buy and short orders based on previous period's indicators, then calculate returns."""
        buy_orders, short_orders = self.allocate_funds(indicators)
        returns = self.calculate_returns(buy_orders, short_orders, start_time, end_time)
        return returns, {'buy': buy_orders, 'short': short_orders}

    def allocate_funds(self, indicators):
        """Allocates funds to buy and sell based on indicators from the last time step using a heap"""
        # Use a heap to store the indicators with their negative values for max-heap functionality
        heap = []
        for ticker, indicator in indicators.items():
            # Push the negative because heapq is a min-heap by nature
            heapq.heappush(heap, (-abs(indicator), ticker, indicator))

        num_to_select = max(1, len(indicators) // 10)  # Trading the top 10% of stocks by indicator magnitude
        buy_orders = {}
        short_orders = {}
        total_magnitude = 0

        # Extract the top indicators from the heap
        top_tickers = [heapq.heappop(heap) for i in range(num_to_select)]
        total_magnitude = sum(-item[0] for item in top_tickers)

        # Calculate proportion of the total value of the portfolio to put towards each trade
        for i, ticker, indicator in top_tickers:
            proportion = abs(indicator) / total_magnitude
            trade_value = self.portfolio_value * proportion
            if indicator > 0:
                buy_orders[ticker] = trade_value
            else:
                short_orders[ticker] = trade_value

        return buy_orders, short_orders

    def calculate_returns(self, buy_orders, short_orders, start_time, end_time):
        """Calculate returns from buy and short positions based on actual price changes"""
        end_prices = self.data.loc[end_time]
        start_prices = self.data.loc[start_time]

        buy_return = sum(((end_prices.get(ticker) / start_prices.get(ticker)) - 1) * amount for ticker, amount in
                                                                                            buy_orders.items())
        short_return = sum((1 - (end_prices.get(ticker) / start_prices.get(ticker))) * amount for ticker, amount in
                                                                                            short_orders.items())

        return self.portfolio_value + buy_return + short_return

    def do_linear_regression(self, ticker, start_time, end_time):
        """Perform linear regression on stock prices to return the slope"""
        prices = self.data[ticker].loc[start_time:end_time].dropna()
        if len(prices) < 2:
            return 0  # Not enough data points for a regression
        x = np.arange(len(prices)).reshape(-1, 1)
        y = prices.values
        model = LinearRegression()
        model.fit(x, y)
        # Slope is used as the indicator to buy or sell for linear regression positive slope = buy; negative = sell
        return model.coef_[0]

    def mean_deviation_indicator(self, ticker, start_time, end_time):
        """Calculate the deviation from the mean for each ticker."""
        prices = self.data[ticker].loc[start_time:end_time].dropna()
        if prices.empty:
            return 0
        mean_price = prices.mean()
        # (-Mean deviation/ mean price) is used as the indicator for mean reversion.
        # If the stock is above the mean price sell and if it is below the mean price buy
        return (mean_price - prices.iloc[-1]) / mean_price

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