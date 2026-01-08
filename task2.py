import csv
from datetime import datetime
# Hardcoded stock prices (edit as you like)
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOG": 140,
    "MSFT": 320,
    "INFY": 1500,
    "RELIANCE": 2900,
    "TCS": 3800
}

def show_menu():
    print("\n=== Stock Portfolio Tracker ===")
    print("1. View available stocks")
    print("2. Buy stock")
    print("3. Sell stock")
    print("4. View current portfolio")
    print("5. Show total investment summary")
    print("6. Save report (TXT & CSV)")
    print("7. Exit")

def view_available_stocks():
    print("\nAvailable stocks and prices (per share):")
    print("-" * 40)
    for symbol, price in STOCK_PRICES.items():
        print(f"{symbol:<10} : {price:>10}")
    print("-" * 40)

def get_quantity():
    try:
        qty = int(input("Enter quantity: ").strip())
        if qty <= 0:
            print("Quantity must be positive.")
            return None
        return qty
    except ValueError:
        print("Please enter a valid integer quantity.")
        return None

def buy_stock(portfolio):
    symbol = input("Enter stock symbol to BUY: ").upper().strip()
    if symbol not in STOCK_PRICES:
        print("Stock not in price list. Please enter a valid symbol.")
        return

    qty = get_quantity()
    if qty is None:
        return

    portfolio[symbol] = portfolio.get(symbol, 0) + qty
    print(f"Bought {qty} shares of {symbol}. Total now: {portfolio[symbol]}")

def sell_stock(portfolio):
    symbol = input("Enter stock symbol to SELL: ").upper().strip()
    if symbol not in portfolio:
        print("You do not own this stock in your portfolio.")
        return

    qty = get_quantity()
    if qty is None:
        return

    if qty > portfolio[symbol]:
        print(f"You only have {portfolio[symbol]} shares of {symbol}. Cannot sell more than you own.")
        return

    portfolio[symbol] -= qty
    if portfolio[symbol] == 0:
        del portfolio[symbol]
        print(f"Sold all shares of {symbol}. It has been removed from your portfolio.")
    else:
        print(f"Sold {qty} shares of {symbol}. Remaining: {portfolio[symbol]}")

def calculate_total_investment(portfolio):
    total = 0
    for symbol, qty in portfolio.items():
        total += STOCK_PRICES[symbol] * qty
    return total

def view_portfolio(portfolio):
    if not portfolio:
        print("\nYour portfolio is empty.")
        return

    print("\nYour Portfolio:")
    print("-" * 60)
    print(f"{'Stock':<10}{'Qty':>8}{'Price':>12}{'Value':>15}")
    print("-" * 60)
    for symbol, qty in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * qty
        print(f"{symbol:<10}{qty:>8}{price:>12}{value:>15}")
    print("-" * 60)

def show_summary(portfolio):
    if not portfolio:
        print("Your portfolio is empty.")
        return

    total = calculate_total_investment(portfolio)
    view_portfolio(portfolio)
    print(f"\nTotal Investment Value: {total}")

def save_report(portfolio):
    if not portfolio:
        print("Portfolio is empty. Nothing to save.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_name = f"portfolio_{timestamp}.csv"
    txt_name = f"portfolio_{timestamp}.txt"

    total = calculate_total_investment(portfolio)

    # Save CSV
    with open(csv_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Quantity", "Price", "Value"])
        for symbol, qty in portfolio.items():
            price = STOCK_PRICES[symbol]
            value = price * qty
            writer.writerow([symbol, qty, price, value])
        writer.writerow([])
        writer.writerow(["TOTAL", "", "", total])

    # Save TXT
    with open(txt_name, mode="w") as txt:
        txt.write("Stock Portfolio Summary\n")
        txt.write("-" * 40 + "\n")
        for symbol, qty in portfolio.items():
            price = STOCK_PRICES[symbol]
            value = price * qty
            txt.write(f"{symbol}: Qty={qty}, Price={price}, Value={value}\n")
        txt.write("-" * 40 + "\n")
        txt.write(f"Total Investment Value: {total}\n")

    print(f"Report saved as: {csv_name} and {txt_name}")

def main():
    portfolio = {}
    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            view_available_stocks()
        elif choice == "2":
            buy_stock(portfolio)
        elif choice == "3":
            sell_stock(portfolio)
        elif choice == "4":
            view_portfolio(portfolio)
        elif choice == "5":
            show_summary(portfolio)
        elif choice == "6":
            save_report(portfolio)
        elif choice == "7":
            print("Exiting Stock Portfolio Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option (1-7).")

if __name__ == "__main__":
    main()
