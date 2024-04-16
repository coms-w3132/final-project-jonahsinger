import matplotlib.pyplot as plt

class BacktestingFramework:
    def __init__(self, tickers, start_date, end_date, amount):
        """
        Initialize the backtesting framework with a list of tickers, start and end dates, and an investment amount.
        :param tickers: List of stock ticker symbols.
        :param start_date: Start date for the data in 'YYYY-MM-DD' format.
        :param end_date: End date for the data in 'YYYY-MM-DD' format.
        :param amount: Initial amount of money to trade with.
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.amount = amount

    def test_linear_regression_strategy(self):
        """
        Test the Linear Regression Strategy and record the performance.
        """
        from LinearRegression import LinearRegressionStrategy  # Import your strategy class
        strategy = LinearRegressionStrategy(self.tickers, self.start_date, self.end_date, self.amount)
        results = strategy.execute_strategy()
        self.plot_results(results, title="Linear Regression Strategy Performance")

    def test_mean_reversion_strategy(self):
        """
        Test the Mean Reversion Strategy and record the performance.
        """
        from MeanReversion import MeanReversionStrategy  # Import your strategy class
        strategy = MeanReversionStrategy(self.tickers, self.start_date, self.end_date, self.amount)
        results = strategy.execute_strategy()
        self.plot_results(results, title="Mean Reversion Strategy Performance")

    def plot_results(self, results, title):
        """
        Plot the results of the trading strategies.
        :param results: Dictionary containing the results of the trading strategies.
        :param title: Title of the plot.
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(results['buy'].keys(), results['buy'].values(), label='Buy Investments', marker='o')
        ax.plot(results['short'].keys(), results['short'].values(), label='Short Investments', marker='x')
        ax.set_title(title)
        ax.set_xlabel('Tickers')
        ax.set_ylabel('Investment Amount ($)')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

