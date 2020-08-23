'''
Author: Fabio Okubo
'''
# from datetime import datetime, date


def date_symbol_exists(date, symbol, data):
    '''
        Check if date and symbol exists in all dictionaries in JSON file
    '''
    for item in data:
        if date == item["Date"] and symbol == item["Symbol"]:
            return True
    return False

# d = [{"Date": 1, "Symbol": "G"}, {"Date": 1, "Symbol": "F"}]    
# print(date_symbol_exists(1, "F", d))

def add_stock(symbol, date, price, data, stock_list):
    '''
        append dictionary to list if it does not exists
    '''
    if date_symbol_exists(date, symbol, data):
        stock_list.append({"Symbol": symbol, "Date": date, "Close": price})
    else:
        stock_list.append({"Symbol": symbol, "Date": date, "Close": 0})
    return stock_list

def get_close_price(symbol, date, data):
    for stock in data:
        if stock["Date"] == date and stock["Symbol"] == symbol:
            return stock["Close"]
    return 0

def search_name(id, data):
    '''
        returns dog name is exists
    '''    
    for item in data:
        if id == item["DogID"]:
            return item["Dog"]
    return None  

def count_unique_symbols(data):
    '''
        returns numbers of unique stock symbols
    '''
    unique_symbols = set()
    for item in data:
        unique_symbols.add(item['Symbol'])
    return len(unique_symbols)

def get_symbols(data):
    '''
        returns list of unique symbols
    '''
    unique_symbols = set()
    for item in data:
        unique_symbols.add(item['Symbol'])
    return list(unique_symbols)

def get_stock_value_history(symbol, shares, data):
    '''
        return a list with all the clock prices
    '''
    close_values = []
    for stock in data:
        if stock["Symbol"] == symbol:            
            close_values.append(round(stock["Close"] * shares, 2))
    
    return close_values

def count_entries(symbol, data):
    '''
        return int on number of times symbol exists
    '''
    count = 0
    for stock in data:
        if stock["Symbol"] == symbol:
            count = count + 1
    return count

#debugging function
def print_from_to(start, end, data):
    '''
        print to screen range of data
    '''
    for i in range(start, end):
        print(data[i]["Symbol"] + ", " + str(data[i]["Date"]) + ", " + str(data[i]["Close"]))