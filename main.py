import sys
import pickle
from datetime import datetime
from src import investment as inv
from src import access

def add_value_to(names):
    opts = 1
    print("Choose investment to update:")
    for name in names:
        print(f'{opts}. {name}')
        opts += 1
        
    inp = input("Enter choice: ")
    return int(inp) - 1

def portfolio_cli(portfolio, file_name):
    while True:
        print("\nOptions:")
        print("1. Plot investment")
        print("2. Plot trends")
        print("3. Add info")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            portfolio.wallet.plot_investments()
        elif choice == "2":
            portfolio.wallet.plot_trends()
        elif choice == "3":
            names = [investment.name for investment in portfolio.wallet.investments]
            idx = add_value_to(names)
            value = float(input("What is your current asset value? "))
            portfolio.wallet.investments[idx].feed_info(value)
            portfolio.wallet.save(file_name)
        elif choice == "4":
            print("Exiting...")
            break

def create_investment():
    name = input("Enter the name of the investment: ")
    risk = input("Enter the risk level of the investment (High/Low/Medium): ")
    invested = float(input("Enter the amount invested: "))
    started_at = datetime.now().strftime("%Y-%m-%d")  # Assuming current date as the start date

    return inv.Investment(name, risk, invested, started_at)

def load_portfolio():
    portfolio_name = input("Enter the name of the portfolio to load: ")
    portfolio = inv.Portfolio(portfolio_name)
    portfolio.read()
    return portfolio, portfolio_name

def main(): 
    granted = access.authorize()
    portfolio = None
    name = None
    if not granted:
        print("Access Denied.")
        sys.exit(0)

    while True:
        print("\nOptions:")
        print("1. Create Investment")
        print("2. Load Investment Portfolio") if portfolio is None else print("2. See more options")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            investment = create_investment()
            if portfolio is not None:
                current_investments = portfolio.wallet.investments
                current_investments.append(investment)  # Append the new investment
                wallet = inv.Wallet(current_investments)  # Initialize Wallet with the updated list
            else:
                wallet = inv.Wallet([investment])
            name = input("Save under what name? ")
            wallet.save(name)
            print("Investment created and saved.")
        elif choice == "2":
            if portfolio is not None:
                portfolio_cli(portfolio, name)
            else:
                portfolio, name = load_portfolio()
        elif choice == "3":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
