import mysql.connector as m
import matplotlib.pyplot as plt
import yfinance as yf
import mplcursors

# Connect to MySQL database
db=m.connect(host='localhost',user='root',password='admin@123')
# Create a cursor object using the cursor() method
c=db.cursor()
# Create a database named StockHive
c.execute("CREATE DATABASE IF NOT EXISTS StockHive")
# Connect to the database
c.execute("USE StockHive")
# Create tables
c.execute(''' CREATE TABLE IF NOT EXISTS Users (
        User_ID INT PRIMARY KEY AUTO_INCREMENT,
        User_Name VARCHAR(50) NOT NULL,
        User_email VARCHAR(30),
        Password VARCHAR(30) UNIQUE)''')
# Create a table named STOCKS
c.execute('''CREATE TABLE IF NOT EXISTS STOCKS (
    User_ID INT,
    Stock_ID INT PRIMARY KEY AUTO_INCREMENT,
    Stock_Name VARCHAR(40) NOT NULL,
    Share_count INT ,
    Purchase_Price FLOAT,
    Purchase_Date DATE,
    Notes VARCHAR(100),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID))''')

# Login function
def Login():
    e=input("Enter email-id: ")
    p=input("Enter password: ")
    c.execute("SELECT * FROM USERS")
    flag=False
    for k in c:
        x=k[2].lower();y=e.lower()
        if x==y and k[3]!=p:
            print("Wrong password entered")
            flag=True
            break
        elif k[3]==p and x!=y:
            print("Wrong email-id entered")
            flag=True
            break
        elif x==y and k[3]==p:
            print("Login Successful")
            flag=True
            break
        elif flag==False:
            print("No matching user found. Kindly recheck the details entered.")
            g=input("Do you want to login again(yes/no):")
            if g.lower()=='yes':
                Login()
            else:
                s=input("Do you want to sign up (yes/no)?")
                if s.lower()=='yes':
                    register_user()
                else:
                    print("Thank you.")
                    break

# Function to register a new user
def register_user():
    print("Registers a new user.")
    user_id=int(input("Enter user id:"))
    user_name=input("Enter user name: ").strip()
    email=input("Enter email ID: ").strip()
    password=input("Enter password: ").strip()
    c.fetchall()
    c.execute("SELECT * FROM Users WHERE User_email=%s",(email,))
    if c.fetchone():
        print("Oops!! Email already exists!!")
    else:
        c.execute("INSERT INTO Users VALUES (%s,%s,%s,%s)",(user_id,user_name,email,password))
        db.commit()
        print("REGISTERED SUCCESSFULLY!!")

# Function to get stock price
def get_stock_price(stock_name):
   try:
       stock_data = yf.Ticker(stock_name)
       current_price = stock_data.history(period="1d")["Close"].iloc[0]
       return current_price
   except IndexError:
       return "Market is closed or no data available."

# Function to add stock
def Add_stock():
    try:
        while c.nextset():
            pass
        u = int(input("Enter user ID: "))
        S = input("Enter Stock name: ")
        s = int(input("Enter number of shares: "))
        pp = int(input("Enter purchase price of stock (in INR): "))
        pd = input("Enter purchase date (YYYY-MM-DD): ")
        n = input("Enter additional notes: ")
        c.fetchall()
        c.execute(
            "INSERT INTO STOCKS (User_ID, Stock_Name, Share_count, Purchase_Price, Purchase_Date, Notes) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (u, S, s, pp, pd, n)
        )
        db.commit()
        print("Stock added successfully!")

    # Handle MySQL errors
    except m.Error as e:
         print("Database error occurred",str(e))
    except ValueError:
        print("Invalid input. Please try again.")
    except Exception as e:
        print("An unexpected error occurred",str(e))

# Function to remove stock
def Remove_stock():
    S=input("Enter Stock name: ")
    P=input("Enter purchase date:")
    c.execute("DELETE FROM STOCKS WHERE Stock_name='{}' AND Purchase_Date='{}'".format(S, P))
    db.commit()
    print("Stock",S,"purchased on",P,"has been deleted.")

# Function to view portfolio
def View_Portfolio(user_id):
    try:
        while c.nextset():
            pass
        
        c.execute("SELECT * FROM STOCKS WHERE User_ID=%s", (user_id,))
        stocks = c.fetchall()
        if stocks:
            # print with proper formatting
            print("{:^30}{:^30}{:^30}{:^30}{:^30}{:^30}{:^30}".format("User_ID","Stock ID","Stock Name","Number of Shares","Purchase Price","Purchase Date","Notes")) 
            for stock in stocks:
                print("{:^20}{:^20}{:^20}{:^20}{:^20}{:^20}{:^20}".format(stock[0],stock[1],stock[2],stock[3],stock[4],stock[5],stock[6]))
        else:
            print("Oops! No stocks found for the given User ID.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function to calculate the total value of the portfolio
def Calculate_Portfolio_Value(user_id):
    try:
        portfolio_value = 0

        # Ensure any previous query's result is cleared
        while c.nextset():
            pass

        c.execute("SELECT * FROM STOCKS WHERE User_ID=%s", (user_id,))
        stocks = c.fetchall()
        if stocks:
            for stock in stocks:
                stock_name = stock[2]
                number_of_shares = stock[3]
                current_price = get_stock_price(stock_name)
                if current_price is not None:
                    portfolio_value += number_of_shares * current_price
            print("Total portfolio value:" ,portfolio_value)
        else:
            print("Oops! No stocks found for the given User ID.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function to calculate the total investment
def Calculate_Total_investment(user_id):
    try:
        total_investment=0
        # Ensure any previous query's result is cleared
        while c.nextset():
            pass
        c.execute("SELECT * FROM STOCKS WHERE User_ID=%s",(user_id,))
        stocks=c.fetchall()
        if stocks:
            for k in stocks:
                Number_of_shares=k[3]
                Purchase_price=k[4]
                total_investment+= Number_of_shares * Purchase_price
            print("Total investment:",total_investment)
            
        else:
            print("Oops! No stocks found for the given User ID.")
    except Exception as e:
        print("An error has occured:",str(e))

# Function to calculate outcome company-wise
def Calculate_outcome_comapnywise():
    try:
        
        # Ensure any previous query's result is cleared
        while c.nextset():
            pass        
        sn=input("Enter stock name: ")
        c.execute("SELECT * FROM STOCKS WHERE Stock_name='{}'".format(sn))
        stocks=c.fetchall()
        if stocks:
            for k in stocks:
                Number_of_shares=k[3]
                Purchase_price=k[4]
                stock_name = k[2]
                current_price=get_stock_price(stock_name)
                if current_price is not None:
                    portfolio_value= Number_of_shares*current_price
                    total_investment= Number_of_shares* Purchase_price
                    pl = portfolio_value - total_investment
                    if pl>0:
                        print("You've made a profit of: ",pl)
                    elif pl==0:
                        print("You've reached a break even point")
                    else:
                        print("You've incurred a loss of: ",pl)
                else:
                    print("Market is closed.Try again later!")
        else:
            print("No stocks found for",sn)
    except Exception as e:
        print("An error has occured:",str(e))

# Function to plot market performance
def plot_market_performance():
    tickers = input("Enter comma-separated ticker symbols: ").split(',')
    period = input("Enter the time period (e.g., 1mo, 6mo, 1y): ")
    plt.figure(figsize=(12, 6))
    for ticker in tickers:
        stock_data = yf.Ticker(ticker.strip())
        history = stock_data.history(period=period)
        # show the closing price of the stock at every point of index
        plt.plot
        plt.plot(history.index, history['Close'], label=ticker.strip())
    plt.title("Market Performance")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    mplcursors.cursor(hover=True)
    plt.show()

def plot_stock_distribution(user_id):
    try:
         # Skip any previous result sets if they exist
        while c.nextset():  
            pass
        # Execute the query to fetch stock details using the existing cursor
        c.execute("SELECT Stock_Name, Share_count, Purchase_Price FROM Stocks WHERE User_ID = %s", (user_id,))
        
        # Now fetch the stock details
        stocks = c.fetchall()

        if stocks:
            labels = []
            sizes = []
            for stock_name, shares, price in stocks:
                labels.append(stock_name)
                sizes.append(shares * price)

            # Plotting the stock distribution
            plt.figure(figsize=(8, 8))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title("Portfolio Stock Distribution")
            mplcursors.cursor(hover=True)
            plt.show()
        else:
            print("No stocks found for the given User ID.")

    except m.Error as e:
        print("Database error occurred:",str(e))
    except Exception as e:
        print("An unexpected error occurred:",str(e))

# Function to calculate daily returns
def plot_daily_returns_histogram(stock_name):
    try:
        # Fetch stock data (adjust period and interval as needed)
        stock_data = yf.Ticker(stock_name)
        historical_data = stock_data.history(period="1y")  
        
        # Calculate daily returns (percentage change)
        historical_data['Daily_Return'] = historical_data['Close'].pct_change() * 100  
        
        # Drop NaN values (first row will be NaN due to pct_change)
        daily_returns = historical_data['Daily_Return'].dropna()

        # Plotting the histogram of daily returns
        plt.figure(figsize=(10, 6))
        plt.hist(daily_returns, bins=50, edgecolor='black', color='skyblue', alpha=0.7)
        plt.title(f"Daily Returns Distribution for {stock_name}")
        plt.xlabel("Daily Return (%)")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print("An error occurred while fetching data:", str(e))


# Function to login or register
def login_or_register():
    """
    Handles user login or registration.
    Returns:
      True if successful login or registration, False otherwise.
    """
    while True:
        choice = input("Do you already have an account (yes/no): ").strip().lower()
        if choice == 'yes':
            Login()
            return True
        elif choice == 'no':
            register_user()
            return True
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Function to display the main menu
def display_menu():
    """
    Displays the main menu options.
    """
    print("\t\t\t\tMENU\t\t\t\t")
    print('''1. \tAdd Stock
            2. Remove Stock
            3. View Portfolio
            4. Calculate Portfolio Value
            5. Calculate Total Investment
            6. Calculate Company-wise Profit/Loss
            7. Stock Price Dynamics
            8. Personal Stock Distribution Chart
            9. Get Stock Price for Desired Company
            10. Daily Returns Histogram
            11. Logout
            12. Quit''')

# Function to handle user choice
def handle_choice(choice):
    """
    Handles the user's menu choice.
    
    """
    try:
        if choice == 1:
            Add_stock()
        elif choice == 2:
            Remove_stock()
        elif choice == 3:
            user_id = int(input("Enter user ID: "))
            View_Portfolio(user_id)
        elif choice == 4:
            user_id = int(input("Enter user ID: "))
            Calculate_Portfolio_Value(user_id)
        elif choice == 5:
            user_id = int(input("Enter user ID: "))
            Calculate_Total_investment(user_id)
        elif choice == 6:
            Calculate_outcome_comapnywise()
        elif choice == 7:
            plot_market_performance()
        elif choice == 8:
            user_id = int(input("Enter user ID: "))
            plot_stock_distribution(user_id)
        elif choice == 9:
            stock_name = input("Enter stock name: ")
            print(get_stock_price(stock_name))
        elif choice == 10:
            stock_name = input("Enter stock symbol (e.g., AAPL): ")
            plot_daily_returns_histogram(stock_name)
        elif choice == 11:
            print("Logging out...")
            main()
            return False
        elif choice == 12:
            print("Exiting...")
            return False
        else:
            print("Invalid input. Please choose a valid option.")
    except ValueError:
        print("Please enter a valid numeric input.")
    return True

# Main function
def main():
    print("\t\t\t\tSTOCKHIVE")
    print("\t\t\tJoin the hive, Master the market")
    print()
    print("\t\t\t\tLOGIN/SIGN UP\t\t\t\t")

    # Login or Register
    if not login_or_register():
        return

    # Display menu and handle user choices
    while True:
        display_menu()
        try:
            choice = int(input("Enter choice: "))
            if not handle_choice(choice):
                break
        except ValueError:
            print("Please enter a valid numeric choice.")

# Run the main function
main()            

                
                                    
                    
                    
                    
                                    
                                    
                                    
                            
            
                            
                            
                            
                            
            
            
            

        
        
        
        


