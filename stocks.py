'''
Author: Fabio Okubo
Date: 7/28/2020
Description:
    Week 7 Assignment
'''
from datetime import date

class Stock:
    ''' stock class '''
    def __init__(self, symbol, purchase_price, current_price, quantity, \
                purchase_date, investor_id, id):
        self.symbol = symbol
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.quantity = quantity
        self.purchase_date = purchase_date
        self.investor_id = investor_id
        self.id = id

    def calculate_earnings(self, current_value, purchase_price, number_of_shares):
        '''returns Calculated earnings/loss
        
        Keyword arguments:
        current_value -- current stock value as int or float
        purchase_price -- purchased stock price as int or float
        number_of_shares -- number of shares as int or float
        '''
        earnings = (current_value - purchase_price) * number_of_shares
        return earnings    

    def calculate_percentage_earnings(self, current_value, purchase_price):
        '''returns Calculated precentage earnings/loss
        
        Keyword arguments:
        current_value -- current stock value as  int or float
        purchase_price -- purchased stock price as  int or float
        '''    
        percentage_earnings = ((current_value - purchase_price) / purchase_price) * 100
        return percentage_earnings      

    def calculate_yearly_earnings(self, current_value, purchase_price, current_date, purchase_date):
        '''returns Calculated yearly earnings/loss

        Keyword arguments:
        current_value -- current stock value as int or float
        purchase_price -- purchased stock price as  int or float
        current_date -- current date as date object
        purchase_date  -- purchase date as date object
        '''
        delta_days = current_date - purchase_date
        delta_days = delta_days.days #convert date obj to int
        number_of_years = delta_days / 365 #total number of days divided by number of day in one year
        
        percentage_earnings = self.calculate_percentage_earnings(current_value, purchase_price)
        yearly_earnings = percentage_earnings / number_of_years
        return yearly_earnings                     


class Bond(Stock):
    ''' bond class '''
    def __init__(self, symbol, purchase_price, current_price, quantity, purchase_date, \
                investor_id, id, coupon, bond_yield):      
        super().__init__(symbol, purchase_price, current_price, quantity, purchase_date, \
                        investor_id, id)
        self.coupon = coupon
        self.bond_yield = bond_yield


class Investor:
    ''' investor class '''
    def __init__(self, investor_id, name, address, phone_number):
        self.investor_id = investor_id
        self.name = name
        self.address = address
        self.phone_number = phone_number