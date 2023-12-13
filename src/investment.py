import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import pickle

class Investment:
    def __init__(self, name: str, risk: str, invested: float, started_at: str):
        self.name = name
        self.risk = risk
        self.invested = invested
        self.started_at = started_at
        self.updated_at = started_at
        self.investment_arr = np.array([self.invested])
        self.trend = np.array([])
        self.dates = [started_at]

    def feed_info(self, value: float, date: str):
        self.investment_arr = np.append(self.investment_arr, value)
        self.dates.append(date)
        size = len(self.investment_arr)
        if size > 1:
            previous_value = self.investment_arr[-2]
            trend = ((value - previous_value) / previous_value) * 100
            self.trend = np.append(self.trend, trend)
            self.updated_at = datetime.now()
        else:
            return 0
        return trend
    
class Portfolio:
    def __init__(self, name, path_to_db='.'):
        self.file_name = name
        self.path_to_db = path_to_db
        self.investments = []

    def read(self):
        try:
            with open(f'{self.path_to_db}/{self.file_name}.pkl', 'rb') as file:
                self.investments = pickle.load(file)
            self.wallet = Wallet(self.investments)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            print(f"Error loading file: {e}")
            self.wallet = Wallet([])  
    

class Wallet:
    def __init__(self, investments):
        self.investments = investments

    def plot_investments(self):
        plt.figure(figsize=(10, 6))
        lengths = [len(investment.investment_arr) for investment in self.investments]
        if min(lengths) != max(lengths):
            print("Error: Investments do not have the same length of data points.")
            return
        
        total_investment = np.zeros(lengths[0])

        for investment in self.investments:
            dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in investment.dates]
            plt.plot(dates, investment.investment_arr, label=investment.name)
            total_investment += investment.investment_arr
            
        plt.plot(dates, total_investment, label='Total Investment', color='black', linewidth=2, linestyle='--')

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

        def currency_formatter(x, pos):
            return f'R$ {x:,.2f}'.replace(',', '.').replace('.', ',')

        plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(currency_formatter))

        plt.title('Investment Over Time')
        plt.xlabel('Date')
        plt.ylabel('Investment Value')
        plt.legend()
        plt.gcf().autofmt_xdate()  # Auto-format the x-axis dates
        plt.show()

    def plot_trends(self):
        plt.figure(figsize=(10, 6))

        for investment in self.investments:
            if len(investment.dates) > 1:  # Ensure there are enough dates for trend calculation
                dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in investment.dates[1:]]  # Skip the first date
                plt.plot(dates, investment.trend, label=investment.name)
                
        def percent_formatter(x, pos):
            return f'{x:.2f}%'

        plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(percent_formatter))


        # Format the x-axis to show dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

        plt.title('Investment Trend Over Time')
        plt.xlabel('Date')
        plt.ylabel('Trend')
        plt.legend()
        plt.gcf().autofmt_xdate()  # Auto-format the x-axis dates
        plt.show()

    def save(self, db_name):
        with open(f'{db_name}.pkl', 'wb') as file:
            pickle.dump(self.investments, file)
        