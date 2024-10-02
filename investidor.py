MAX_NUMBER_OF_ASSETS = 5

class Investor:
    def __init__(self, initial_money, estrategy:dict) -> None:
        self.money = initial_money
        self.estrategy = estrategy
        self.wallet = {}
        
    def get_heritage(self, actual_stocks_prices:dict) -> float:
        heritage = self.money
        for key in self.wallet:
            heritage += round(self.wallet[key] * actual_stocks_prices[key],6)  
        return heritage 
    
    def rebalance_wallet(self, actual_stocks_prices:dict) -> None:
        if len(self.wallet) > 1:
            for key in self.wallet.keys():
                self.money += round(self.wallet[key]*actual_stocks_prices[key],6)
            
            #dividir o dinheiro total igualmente pelos ativos
            money_for_each_stock = round(self.money/len(self.wallet),6)
            
            if money_for_each_stock > 0:
                for key in self.wallet.keys():
                    self.wallet[key] = round(money_for_each_stock/actual_stocks_prices[key],6)
            
            self.money = 0
               
    def search_stock_to_sell(self, actual_stocks_prices:dict, fair_stock_prices:dict) -> None:
        new_wallet = {}
        for key in self.wallet.keys():
            if actual_stocks_prices[key] > self.estrategy['sell'] * fair_stock_prices[key]:
                self.money += round(self.wallet[key] * actual_stocks_prices[key],6)
            else:
                new_wallet[key] = self.wallet[key]
        
        self.wallet = new_wallet
                       
    def search_stock_to_buy(self, actual_stocks_prices:dict, fair_stock_prices:dict) -> None:
        if self.money > 0:
            under_price = {}
            
            for key in actual_stocks_prices:
                if (actual_stocks_prices[key] < self.estrategy['buy'] * fair_stock_prices[key]):
                    under_price[key] = actual_stocks_prices[key]/fair_stock_prices[key]
            
            #ordenar pela mais baratas relativamente
            ordened_under_price = sorted(under_price.items(), key=lambda item: item[1])
            
            #descobrir a quantidade de ativos que ainda pode comprar
            wallet_vacance = MAX_NUMBER_OF_ASSETS - len(self.wallet)
            
            if wallet_vacance > 0:
                money_for_each_stock = round(self.money/wallet_vacance,6)
            
                for item in ordened_under_price:
                    key = item[0]
                    
                    if key not in self.wallet.keys():
                        self.wallet[key] = round(money_for_each_stock / actual_stocks_prices[key],6)
                        self.money -= money_for_each_stock 
                        if self.money == 0: break   
                        
          
                    
        