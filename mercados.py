import random

GRAHAM_AVERAGE = 1.0
GRAHAM_INTERVAL = 0.5
MININUM_GRAHAM_RATIO = 0.4
MAXIMUM_GRAHAM_RATIO = 2.0

MAXIMUM_MONTH_STOCK_VARIATION = 0.1
ANUAL_STOCK_VOLABILITY = 0.05
MONTHLY_CONTROL_LIMIT = 0.05
# para garantir que o valor real pertença a [0.5*graham,1.5*graham] com 99,7% de certeza, (1.5-1)*graham deve ser 3 sigma
# logo sigma = graham_interval / 3

class Market:
    def __init__(self ,seed, number_of_stocks):
        self.volativity_month = (1+ANUAL_STOCK_VOLABILITY)**(1/12) - 1
        self.number_of_stocks_in_market = number_of_stocks
        self.fair_stock_prices = {}
        self.real_stock_prices = {}
        random.seed(seed)
        self.generate_new_graham_values()
        self.generate_initial_real_stock_prices()
        
    def get_real_stock_prices(self):
        return self.real_stock_prices.copy()
    
    def get_fair_stock_prices(self):
        return self.fair_stock_prices.copy()
    
    def update_real_stock_prices(self):
        for key in self.real_stock_prices.keys():
            anual_necessary_readjustment = (self.fair_stock_prices[key] - self.real_stock_prices[key])/self.real_stock_prices[key]
            monthy_necessary_readjustment = (1+anual_necessary_readjustment)**(1/12) - 1
            monthly_variation = random.normalvariate(monthy_necessary_readjustment, MONTHLY_CONTROL_LIMIT/3)
            thresholded_monthly_variation = max(monthly_variation-MAXIMUM_MONTH_STOCK_VARIATION,min(monthly_variation,monthly_variation+MAXIMUM_MONTH_STOCK_VARIATION))
            self.real_stock_prices[key] = round(self.real_stock_prices[key] * (1 + thresholded_monthly_variation),6)
    
    def update_fair_stock_prices(self):        
        for i in range(self.number_of_stocks_in_market):
            #self.fair_stock_prices[i] = self.fair_stock_prices[i]*((1+self.volativity_month)**12)
            variation = random.normalvariate(ANUAL_STOCK_VOLABILITY, MONTHLY_CONTROL_LIMIT/3)
            #thresholded_variation = max(-0.2,min(random.normalvariate(ANUAL_STOCK_VOLABILITY, MONTHLY_CONTROL_LIMIT/3),0.2))
            self.fair_stock_prices[i] = self.fair_stock_prices[i]*(1+variation)
            
    def generate_new_graham_values(self, months = 0):
        small_price = 2.0*((1+self.volativity_month)**(months))
        high_price = 100.0*((1+self.volativity_month)**(months))
        for i in range(self.number_of_stocks_in_market):
            self.fair_stock_prices[i] = random.uniform(small_price, high_price)
            
    def generate_initial_real_stock_prices(self):
        for i in range(self.number_of_stocks_in_market):
            graham_value = random.normalvariate(GRAHAM_AVERAGE, GRAHAM_INTERVAL/3)
            #thresholded_graham_value = max(MININUM_GRAHAM_RATIO,min(graham_value,MAXIMUM_GRAHAM_RATIO))
            self.real_stock_prices[i] = round(graham_value * self.fair_stock_prices[i],6)
            
            
            