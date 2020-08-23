'''
Author: Fabio Okubo
Date: 8/22/2020
version: 1
Description:
    Week 10 Portfolio assignment
'''
import database as db
import uuid #to generate unique transaction numbers
from datetime import datetime, date
from stocks import Stock, Bond, Investor
from prettytable import PrettyTable
import json
from stock_functions import add_stock, get_close_price, get_stock_value_history,date_symbol_exists
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from stock_comparison import compare_tickers




def week_8():
    '''
    create accounts database, within accounts.db there will be 3 tables:
        investor, stock, bond
    '''
    #database name
    current_date = date.today() 
    db_name = "accounts.db"
    table_name = "investor"
    db_table_headers = """
                        investor_id text, 
                        name text, 
                        address text, 
                        phone_number text
                        """
                    
    #create_table investor table if it does not exist
    db.create_table(db_name, table_name, db_table_headers)
    #create instance of Investor Object uuid generates unique ID in hex format as string
    investor = Investor(uuid.uuid1().hex, "Bob Smith", 
                        "2199 S University Blvd, Denver, CO 80208", "303-871-2000")
    #content to add to database record
    content = (investor.investor_id, investor.name, investor.address, investor.phone_number)
    #create record in investor table
    db.add_one(db_name, table_name, content)
    #date object with today's date
    print()
    #[0][0]access first list and first tuple itme in db query
    print("Investor Name: " + db.get_selected_data(db_name, table_name, "name")[0][0])
    print("Investor Address: " + db.get_selected_data(db_name, table_name, "address")[0][0])
    print("Investor Phone: " + db.get_selected_data(db_name, table_name, "phone_number")[0][0])
    '''
    ====================================================================
    STOCK SECTION
    ====================================================================
    '''
    #declare variables
    sub_header = []
    stocks = []  #stores stock object(s)
    stock_file = "Lesson6_Data_Stocks.csv"

    #opening stock file
    try:
        read_file = open(stock_file, "r")
    except FileNotFoundError:
        print("Could not open the file, program terminated! I'll be back!")
        exit()  #exit application if file cannot be found        

    #create list of items separated by comma delimiters
    sub_header = read_file.readline().split(',')
    #remove the '\n' character at the end of the line
    sub_header[-1] = sub_header[-1][:-1]
    #add investor id to subheader list
    sub_header.append("investor_id")

    #create stocks table in database
    db_name = "accounts.db"
    table_name = "stocks"
    #sub_header = [0] = SYMBOL, [1] = NO_SHARES, [2] = PUR_PRICE, [3] = CUR_VALUE, [4] = PUR_DATE 
    db_table_headers = "investor_id text, stock_id text," + sub_header[0] + " text, "   \
                        + sub_header[1] + " integer, " + sub_header[2] + " real, "      \
                        + sub_header[3] + " real, " + sub_header[4] + " text" 

    #create_table investor table if it does not exist
    db.create_table(db_name, table_name, db_table_headers)

    #read data from stock file and store in stocks[]
    for line in read_file:
        line_split = line.split(',')
        #removed the '/n' from the last item
        line_split[-1] = line_split[-1][:-1]
        symbol = line_split[0]
        quantity = int(line_split[1])  
        purchase_price = float(line_split[2])
        current_price = float(line_split[3])      
        #converts string formated as MM/DD/YYYY to date object  
        purchase_date = datetime.strptime(line_split[4], '%m/%d/%Y').date()  
        #create object and appends to list
        stock = Stock(symbol, purchase_price, current_price,quantity,purchase_date, \
            investor.investor_id, uuid.uuid1().hex ) #uuid generates unique transaction number
        stocks.append(stock)
        #add record to database
        content = (investor.investor_id, 
                        stock.id,
                        stock.symbol,
                        stock.quantity ,
                        stock.purchase_price,
                        stock.current_price,
                        stock.purchase_date)
        #create record in investor table
        db.add_one(db_name, table_name, content)
    read_file.close()

    #sub_header = [0] = SYMBOL, [1] = NO_SHARES, [2] = PUR_PRICE, [3] = CUR_VALUE, [4] = PUR_DATE 
    data = db.get_selected_data(db_name,"stocks", sub_header[0] + ", " + sub_header[1] + ", " + \
        sub_header[2] + ", " + sub_header[3] + ", " + sub_header[4])

    #print table stock table
    print()
    print("=================== Stock Positions ===================")
    stock_table = PrettyTable()
    stock_table.field_names = [sub_header[0], sub_header[1], "Earnings/Loss", "Yearly Earning/Loss"]
    for row in data:
        #instance of stock class
        stock = Stock(row[0],row[2],row[3],row[1],row[4], None, None)
        earnings = round(stock.calculate_earnings(row[3], row[2], row[1]), 2)
        purchase_date = datetime.strptime(row[4], '%Y-%m-%d').date()
        yearly_earnings = round(stock.calculate_yearly_earnings(row[3], row[2], \
            current_date, purchase_date), 2)
        stock_table.add_row([row[0], row[1], "$ {:,.2f}".format(earnings), str(yearly_earnings) + " %"])

    print(stock_table)

    '''
    =============================================================
    Week 8 JSON to DB
    =============================================================
    '''
    filename = "AllStocks.json"
    dates = []
    transactions = []
    symbols = ["GOOG", "MSFT", "RDS-A", "AIG", "FB", "M", "F", "IBM"]
    db_name = "accounts.db"
    table_name = "json_data"
    db_table_headers = """
                        Symbol text, 
                        Date text, 
                        Open text, 
                        High text,
                        Low text,
                        Close real,
                        Volume integer
                        """

    #load JSON file
    try:
        with open(filename) as f:
            stocks = json.load(f)
    except FileNotFoundError:
        print("Could not find file")
        exit()   

    # #create database
    db.create_table(db_name, table_name, db_table_headers)

    #pass informatiom from JSON to DB
    for stock in stocks:
        content = (
            stock["Symbol"],
            stock["Date"],
            stock["Open"],
            stock["High"],
            stock["Low"],
            stock["Close"],
            stock["Volume"]
        )
        db.add_one(db_name,table_name, content)

    for stock in stocks:
        #convert date string to date object
        purchase_date = datetime.strptime(stock["Date"], '%d-%b-%y').date()  
        transactions.append(
            {
                "Symbol" : stock["Symbol"], 
                "Date": purchase_date, 
                "Close": float(stock["Close"])      
            }
        )

    # creates lists with all the different dates
    for stock in transactions:
        date = stock["Date"]
        if date in dates:
            pass
        else:
            dates.append(date)    

    dates = sorted(dates)        


    #hold total portifolio value per day
    total = []
    #make data symetrical so it can be graphed
    data_to_graph = []
    for date in dates:
        for symbol in symbols:
            close_price = get_close_price(symbol, date, transactions)
            data_graph = add_stock(symbol, date, close_price, 
                transactions, data_to_graph)
            total
            
    data_to_graph = sorted(data_to_graph, key = lambda stock: (stock['Symbol'], stock['Date'])) 

    plt.plot(dates, get_stock_value_history("GOOG",125, data_to_graph))
    plt.plot(dates, get_stock_value_history("MSFT",85, data_to_graph))
    plt.plot(dates, get_stock_value_history("RDS-A",400, data_to_graph))
    plt.plot(dates, get_stock_value_history("AIG", 235, data_to_graph))
    plt.plot(dates, get_stock_value_history("FB", 150, data_to_graph))
    plt.plot(dates, get_stock_value_history("M", 425, data_to_graph))
    plt.plot(dates, get_stock_value_history("F", 85, data_to_graph))
    plt.plot(dates, get_stock_value_history("IBM", 80, data_to_graph))

    plt.legend(symbols) 
    plt.title("Stock Positions")
    plt.ylabel('Value in Dollars')
    plt.xlabel("Date")
    plt.savefig('stock_positions.png')
    plt.show()


    '''
    ====================================================================
    BOND SECTION
    ====================================================================
    '''
    sub_header = []
    bonds = []  #hold bond object(s)
    bond_file = "Lesson6_Data_Bonds.csv"
    #try opening stock file
    try:
        read_file = open(bond_file, "r")
    except FileNotFoundError:
        print("Could not open the file, program terminated! I'll be back!")
        exit()  #exit application if file cannot be found  

    sub_header = read_file.readline().split(',')
    #remove the '\n' character at the end of the line
    sub_header[-1] = sub_header[-1][:-1]

    #create bonds table in database
    db_name = "accounts.db"
    table_name = "bonds"
    #sub_header = [0] = SYMBOL, [1] = NO_SHARES, [2] = PUR_PRICE, [3] = CUR_VALUE, [4] = PUR_DATE 
    #[5] = COUPON, [6] = YIELD
    db_table_headers = "investor_id text, bond_id text," + sub_header[0] + " text, "   \
                        + sub_header[1] + " integer, " + sub_header[2] + " real, "     \
                        + sub_header[3] + " real, " + sub_header[4] + " text,"         \
                        + sub_header[5] + " real, " + sub_header[6] + " real" 

    #create_table investor table if it does not exist
    db.create_table(db_name, table_name, db_table_headers)

    #read data from bond file and store in bonds[]
    for line in read_file:
        line_split = line.split(',')
        #removed the '/n' from the last item
        line_split[-1] = line_split[-1][:-1]
        symbol = line_split[0]
        quantity = int(line_split[1])  
        purchase_price = float(line_split[2])
        current_price = float(line_split[3])   
        #converts string formated as MM/DD/YYYY to date object  
        purchase_date = datetime.strptime(line_split[4], '%m/%d/%Y').date()  
        coupon = float(line_split[5])  
        bond_yield = float(line_split[6])  
        bond = Bond(symbol, purchase_price, current_price,quantity, purchase_date, 
                investor.investor_id, uuid.uuid1().hex, coupon, bond_yield)
        bonds.append(bond)
        #add record to database
        content = (investor.investor_id, 
                    bond.id,
                    bond.symbol,
                    bond.quantity,
                    bond.purchase_price,
                    bond.current_price,
                    bond.purchase_date,
                    bond.coupon,
                    bond.bond_yield
                    )
        #create record in investor table
        db.add_one(db_name, table_name, content)
    read_file.close()

    #sub_header = [0] = SYMBOL, [1] = NO_SHARES, [2] = PUR_PRICE, [3] = CUR_VALUE, [4] = PUR_DATE 
    # [5] = COUPON, [6] = YIELD
    data = db.get_selected_data(db_name,"bonds",                             \
                                sub_header[0] + ", " + sub_header[1] + ", " + \
                                sub_header[2] + ", " + sub_header[3] + ", " + \
                                sub_header[4] + ", " + sub_header[5] + ", " + \
                                sub_header[6])

    #print table bond table
    print()
    print("=================== Bond Positions ===================")
    bond_table = PrettyTable()
    bond_table.field_names = [sub_header[0], sub_header[1], "Earnings/Loss", \
        "Yearly Earning/Loss", sub_header[5], sub_header[6]]
    for row in data:
        #instance of stock class
        #[0] = SYMBOL, [1] = NO_SHARES, [2] = PUR_PRICE, [3] = CUR_VALUE, [4] = PUR_DATE 
        #[5] = COUPON, [6] = YIELD
        bond = Bond(row[0], row[2], row[3],row[1],row[4], None, None, row[5], row[6])
        earnings = round(bond.calculate_earnings(row[3], row[2], row[1]), 2)
        purchase_date = datetime.strptime(row[4], '%Y-%m-%d').date()
        yearly_earnings = round(bond.calculate_yearly_earnings(row[3], row[2], \
            current_date, purchase_date), 2)
        #[0] = SYMBOL, [1] = NO_SHARES, [5] = COUPON, [6] = YIELD        
        bond_table.add_row([row[0], row[1], "$ {:,.2f}".format(earnings), \
            str(yearly_earnings) + " %", row[5], row[6]])

    print(bond_table)


def main():
    while True:
        print("Menu: ")
        print("1. Press \"1\" to compare stocks")
        print("2. Press \"2\" to run week 8 program")
        print("3. Press \"Q\" to quit")
        #grab user input and change to upper case if letter
        user_input = input("Enter choice: ").upper()
        if user_input ==  "Q":
            print("Good Bye!!!")
            exit()
        elif user_input == "2":
            week_8()
            exit()
        elif user_input == "1":
            compare_tickers()
            exit()

if __name__ == "__main__":
    main()