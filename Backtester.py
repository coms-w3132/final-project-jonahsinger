"""
This class contains the backtester methods for the four strategies:
1. Linear Regression
2. Mean Reversion
3. Median Reversion with Binary Search Tree
4. Combined Short and long term analysis strategy with mean reversion and linear regression

Each strategy generates a dictionary with keys/stocks and values/indicators.
The backtester buys and sells stocks based on the indicators that each trading
strategy generates. The larger the magnitude of the indicator the more funds
that are allocated to buying or selling the stock. Positive indicator indicates
a recommended buy and negative indicates a recommended sell. The backtester
calculates the returns of the trades over many time steps and plots the results.
All strategies use the real price data to generate indicators and the returns are
calculated from the actual price movements of the stocks. Data is from yfinance.

These strategies can be run and the parameters can be modified in the files:
LinearRegression.py
MeanReversion.py
MedianReversion.py
ShortLongTerm.py
"""

import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import heapq
from BST import BST


class Backtester:
    def __init__(self, tickers, start_date, end_date, amount):
        self.tickers = tickers  # Stock symbols
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.amount = amount  # Starting money
        self.data = self.get_stock_data()  # Gets price data
        self.portfolio_value = self.amount
        # Dictionaries to store indicators for each strategy
        self.previous_slopes = {}
        self.previous_mean_deviations = {}
        self.previous_median_deviations = {}
        self.previous_combined_indicators = {}

    def get_stock_data(self):
        """Gets data for the specified tickers in the date range from yfinance"""
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
        print(data['Close'].dropna(how='all'))  # prints a sample of the data
        return data['Close'].dropna(how='all')  # drops null data

    def run_strategy(self, step_size, strategy):
        """Executes the specified trading strategy over defined period."""
        trading_days = self.data.index
        start_idx = 0
        value_history = [(trading_days[start_idx], self.portfolio_value)]

        # Loops until the end of trading days
        while start_idx < len(trading_days):
            # Calculates start_time and end_time for the current step
            end_idx = min(start_idx + step_size, len(trading_days) - 1)
            start_time, end_time = trading_days[start_idx], trading_days[end_idx]

            # Buys and sells stocks based off of indicators from previous step and calculates returns
            if start_idx > 0:  # No trades are placed on first step because there is no prior data

                # Call preform step function with proper previous indicators
                if (strategy == "linear regression") or (strategy == "reverse linear regression"):
                    current_value, investments = self.perform_step(start_time, end_time, self.previous_slopes)
                elif (strategy == "mean reversion") or (strategy == "reverse mean reversion"):
                    current_value, investments = self.perform_step(start_time, end_time, self.previous_mean_deviations)
                elif (strategy == "median reversion") or (strategy == "reverse median reversion"):
                    current_value, investments = self.perform_step(start_time, end_time,
                                                                   self.previous_median_deviations)
                elif (strategy == "short and long term") or (strategy == "reverse short and long term"):
                    current_value, investments = self.perform_step(start_time, end_time,
                                                                   self.previous_combined_indicators)
                else:
                    print("Invalid strategy")
                    current_value = 0
                    investments = 0

                # Print all trades and their returns for the most recent time step
                print(f"\nFrom {start_time.date()} to {end_time.date()}:")
                print("Trades executed:")
                for trade_type, orders in investments.items():
                    print(f"{trade_type.capitalize()}:")
                    for ticker, amount in orders.items():
                        print(f"  {ticker}: ${amount:.2f}")
                print(f"Return after this period: ${current_value - self.portfolio_value:.2f}")

                self.portfolio_value = current_value  # updates portfolio value
                if self.portfolio_value <= 0:
                    quit("Portfolio value zero or negative")
                value_history.append((end_time, self.portfolio_value))  # updates value history for graphing later

            # After the step is preformed: Update indicators for the next period
            # Dictionary mapping strategies to their respective functions, indicators, and a reverse multiplier
            strategy_config = {
                "linear regression": (self.linear_regression_indicator, 'previous_slopes', 1),
                "reverse linear regression": (self.linear_regression_indicator, 'previous_slopes', -1),
                "mean reversion": (self.mean_deviation_indicator, 'previous_mean_deviations', 1),
                "reverse mean reversion": (self.mean_deviation_indicator, 'previous_mean_deviations', -1),
                "median reversion": (self.median_deviation_indicator, 'previous_median_deviations', 1),
                "reverse median reversion": (self.median_deviation_indicator, 'previous_median_deviations', -1),
                "short and long term": (self.combined_indicator, 'previous_combined_indicators', 1),
                "reverse short and long term": (self.combined_indicator, 'previous_combined_indicators', -1)
            }

            # Executes the strategy and updates indicators
            if strategy in strategy_config:
                func, attr, multiplier = strategy_config[strategy]
                # Calculates indicators for each ticker and stores them in the appropriate attribute
                updated_indicators = {}
                for ticker in self.tickers:
                    # Updates the indicator by calling the appropriate function
                    # Strategy is reversed by switching sign of indicator
                    updated_indicators[ticker] = multiplier * func(ticker, start_time, end_time)
                setattr(self, attr, updated_indicators)
            else:
                print("Invalid strategy")

            # Shifts to the next time step
            start_idx = end_idx + 1

        # When at the end of trading days plot results
        self.plot_results(value_history, strategy, self.start_date, self.end_date, step_size)

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

        # Extract the top indicators from the heap
        top_tickers = [heapq.heappop(heap) for _ in range(num_to_select)]
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
        """Calculates returns from buy and short positions based on actual price changes"""
        end_prices = self.data.loc[end_time]
        start_prices = self.data.loc[start_time]

        buy_return = sum(((end_prices.get(ticker) / start_prices.get(ticker)) - 1) * amount for ticker, amount in
                         buy_orders.items())
        short_return = sum((1 - (end_prices.get(ticker) / start_prices.get(ticker))) * amount for ticker, amount in
                           short_orders.items())

        return self.portfolio_value + buy_return + short_return

    def linear_regression_indicator(self, ticker, start_time, end_time):
        """Performs linear regression on stock prices to return the slope"""
        prices = self.data[ticker].loc[start_time:end_time].dropna()
        if len(prices) < 2:
            return 0  # Not enough data points for a regression
        x = np.arange(len(prices)).reshape(-1, 1)
        y = prices.values
        model = LinearRegression()
        model.fit(x, y)
        # Slope is used as the indicator to buy or sell for linear regression positive slope = buy; negative = sell
        # Slope is divided by last price to make indicators meaningfully comparable
        return model.coef_[0]/prices.iloc[-1]

    def mean_deviation_indicator(self, ticker, start_time, end_time):
        """Calculate the deviation from the mean for a ticker"""
        prices = self.data[ticker].loc[start_time:end_time].dropna()
        if prices.empty:
            return 0
        mean_price = prices.mean()
        # (-Mean deviation/ mean price) is used as the indicator for mean reversion.
        # If the stock is above the mean price sell and if it is below the mean price buy
        # The deviation is divided by mean price to make indicators meaningfully comparable
        last_price = prices.iloc[-1]
        return (mean_price - last_price) / mean_price

    def median_deviation_indicator(self, ticker, start_time, end_time):
        """Calculate the deviation from the median for a ticker using BST with in-order traversal."""
        prices = self.data[ticker].loc[start_time:end_time].dropna()
        if prices.empty:
            return 0  # Return 0 deviation if no prices are available

        bst = BST()
        root = None
        # Insert all price data into the BST
        for price in prices:
            root = bst.insert(root, price)  # Always update the root in case it changes

        # Find the median using in-order traversal
        median_price = bst.find_median(root)
        if median_price is None:
            return 0  # Return 0 deviation if median calculation fails

        # (-Median deviation/ median price) is used as the indicator for median reversion.
        # If the stock is above the median price sell and if it is below the median price buy
        # The deviation is divided by median price to make indicators meaningfully comparable
        last_price = prices.iloc[-1]
        return (median_price - last_price) / median_price

    def combined_indicator(self, ticker, start_time, end_time):
        """Uses the linear regression over the long term and mean deviation over the short term"""
        # Uses last five days for mean reversion indicator
        period_for_mean = end_time - pd.Timedelta(days=5)
        mean_deviation_indicator = self.mean_deviation_indicator(ticker, period_for_mean, end_time)

        # Uses the entire step size for linear regression indicator
        linear_regression_indicator = self.linear_regression_indicator(ticker, period_for_mean, end_time)

        # Adds indicators together
        combined_value = mean_deviation_indicator + linear_regression_indicator
        return combined_value

    def plot_results(self, value_history, strategy, start_date, end_date, step_size):
        """Plot the value of the portfolio over time with appropriate title."""
        dates, values = zip(*value_history)
        plt.figure(figsize=(10, 5))
        plt.plot(dates, values, 'o-')
        title = f"{strategy.title()} Strategy: {start_date.date()} to {end_date.date()}, Step Size: {step_size}"
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value ($)")
        plt.grid(True)
        plt.show()
