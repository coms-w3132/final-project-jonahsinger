import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

class Backtester:
    def __init__(self, tickers, start_date, end_date):
        """
        Initializes a backtester with tickers over a range start_date-end_date
        :param tickers: List of stock ticker symbols
        :param start_date: String, start date for the data in 'YYYY-MM-DD' format
        :param end_date: String, end date for the data in 'YYYY-MM-DD' format
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.download_data()
        self.cash = 1000000  # Starts with 1 million dollars
        self.holdings = {ticker: 0 for ticker in tickers}  # Track number of shares held for each ticker
        self.portfolio_value = []

    def download_data(self):
        """
        Download stock data for the tickers and timeframe using yfinance.
        """
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
        return data['Adj Close']

    def buy(self, amount, date):
        """
        Buy stocks with the given amount of dollars.
        """
        available_cash = min(amount, self.cash)
        amount_per_stock = available_cash / len(self.tickers)
        for ticker in self.tickers:
            if amount_per_stock > 0:
                price = self.data[ticker].loc[date]
                shares_to_buy = amount_per_stock / price
                self.holdings[ticker] += shares_to_buy
                self.cash -= shares_to_buy * price

    def sell(self, amount, date):
        """
        Sell stocks with the given amount of dollars.
        """
        amount_per_stock = amount / len(self.tickers)
        for ticker in self.tickers:
            price = self.data[ticker].loc[date]
            shares_to_sell = min(self.holdings[ticker], amount_per_stock / price)
            self.holdings[ticker] -= shares_to_sell
            self.cash += shares_to_sell * price

    def calculate_portfolio_value(self, date):
        """
        Calculate the current value of the portfolio based on holdings and market data.
        """
        total_value = self.cash
        for ticker, shares in self.holdings.items():
            price = self.data[ticker].loc[date]
            total_value += shares * price
        self.portfolio_value.append(total_value)
        return total_value

    def close_all_positions(self, date):
        """
        Close all positions to exit the market by selling all holdings.
        """
        for ticker in self.tickers:
            price = self.data[ticker].loc[date]
            self.cash += self.holdings[ticker] * price
            self.holdings[ticker] = 0
        self.portfolio_value.append(self.cash)

    def plot_portfolio_value(self):
        """
        Plot the daily total value of the portfolio.
        """
        plt.figure(figsize=(10, 5))
        plt.plot(self.portfolio_value, label='Portfolio Value')
        plt.title('Portfolio Value Over Time')
        plt.xlabel('Day')
        plt.ylabel('Total Value ($)')
        plt.legend()
        plt.grid(True)
        plt.show()

