"""
Example test runs for linear regression strategy and reverse linear regression strategy
Parameters: tickers, start_date, end_date, amount (starting cash), and step_size can be modified.
"""

from Backtester import Backtester


def main():
    """Tests 2 runs of linear regression and reverse linear regression"""
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'T', 'VZ', 'AMZN', 'META', 'TSLA', 'NVDA', 'INTC', 'AMD',
        'IBM', 'CSCO', 'ORCL', 'ADBE', 'CRM', 'NFLX', 'DIS', 'PFE', 'JNJ', 'GILD', 'NKE',
        'KO', 'PEP', 'MCD', 'WMT', 'TGT', 'COST', 'CVX', 'XOM', 'BP', 'T', 'VZ',
        'TMUS', 'BA', 'LMT', 'NOC', 'BABA', 'JD', 'V', 'MA', 'JPM', 'GS', 'BAC', 'C',
        'WFC', 'BLK', 'AXP', 'GE', 'GM', 'F', 'DAL', 'UAL', 'AAL', 'LUV', 'EA', 'TTWO', 'SPG',
        'AMT', 'PLD', 'CCI', 'D', 'SO', 'XEL', 'NEE', 'GSK', 'CVS', 'WBA', 'TMO', 'ABT', 'LHX',
        'GD', 'TXT', 'HON', 'UNH', 'MCK', 'MO', 'PM', 'STZ', 'BTI', 'CL', 'PG', 'UL', 'EL',
        'ADM', 'ADP', 'BIIB', 'BLK', 'CAH', 'CAT', 'COP', 'DD', 'ECL', 'F', 'PFE', 'SLB', 'TXN', 'V',
        'RTX', 'SPGI', 'LOW', 'GS', 'ISRG', 'HON', 'AXP', 'INTC', 'INTU', 'BMY', 'IBM', 'QCOM', 'GE', 'DE'
    ]
    start_date = '2014-10-01'
    end_date = '2024-04-21'
    step_size = 60  # How often linear regression is taken and stocks are bought and sold
    amount = 10000
    backtester = Backtester(tickers, start_date, end_date, amount)
    backtester.run_strategy(step_size, "linear regression")
    backtester.portfolio_value = 10000
    backtester.run_strategy(step_size, "reverse linear regression")

    step_size = 5
    backtester.portfolio_value = 10000
    backtester.run_strategy(step_size, "linear regression")
    backtester.portfolio_value = 10000
    backtester.run_strategy(step_size, "reverse linear regression")


if __name__ == "__main__":
    main()
