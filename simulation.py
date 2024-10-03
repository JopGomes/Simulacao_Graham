import random
from investidor import Investor
from mercados import Market
from estatistica import show_statistics
import numpy as np

INITIAL_MONEY = 1000
NUMBER_OF_SIMULATIONS = 100
NUMBER_OF_YEARS = 10
NUMBER_OF_MONTHS = 12 * NUMBER_OF_YEARS
SEED = 42
NUMBER_OF_STOCKS = 50

def generate_estrategies() -> list[dict]:
    smallest_buy_limit = 0.5
    biggest_buy_limit = 1.2
    step = 0.01
    smallest_sell_limit = 0.90
    biggest_sell_limit = 1.5
    step = 0.05
    actual_buy_limit = smallest_buy_limit
    estragies = []
    
    while actual_buy_limit <= biggest_buy_limit:
        actual_sell_limit = smallest_sell_limit
        while actual_sell_limit <= biggest_sell_limit:
            if actual_buy_limit < actual_sell_limit:
                estragies.append({'buy':actual_buy_limit, 'sell':actual_sell_limit})
            actual_sell_limit+=step
        actual_buy_limit+=step
    print(estragies[85])
    print(estragies[86])
    print(estragies[96])
    print(estragies[97])
    print(estragies[107])
    return estragies

def generate_markets() -> list[Market]:
    markets = []
    random.seed(SEED)
    numeros_aleatorios = [random.randint(1, 100000) for _ in range(NUMBER_OF_SIMULATIONS)]
    
    for i in range(NUMBER_OF_SIMULATIONS):
        markets.append(Market(numeros_aleatorios[i],NUMBER_OF_STOCKS))   
        
    return markets      

def generate_investors(estrategies:list[dict]) -> list[Investor]:
    investors = []
    for estrategy in estrategies:
        investors.append(Investor(INITIAL_MONEY, estrategy))
        
    return investors
       
def calculate_heritage_of_investors(investors:list[Investor],stocks_prices:dict) -> list[float]:
    result = []   
    for investor in investors:
        result.append(investor.get_heritage(stocks_prices)) 
        
    return result   
        
def run_one_simulation(investors:list[Investor], market:Market) -> list[dict]:
    real_stock_prices = []

    for month in range(0,NUMBER_OF_MONTHS):
        fair_stock_prices = market.get_fair_stock_prices()
        real_stock_prices.append(market.get_real_stock_prices())
        
        for investor in investors:
            investor.search_stock_to_sell(real_stock_prices[month], fair_stock_prices)
            investor.search_stock_to_buy(real_stock_prices[month], fair_stock_prices)
            
            if (month + 1) % 6 == 0:
                investor.rebalance_wallet(real_stock_prices[month])
            
        if (month + 1) % 12 == 0:
            market.update_fair_stock_prices()
        
        market.update_real_stock_prices()
    
    return real_stock_prices
      
def run_all_simulations(markets:list[Market], estrategies:list[dict]) -> list[float]:
    results = []
    evolution = []
    
    for market in markets:
        investors = generate_investors(estrategies)  
        stocks_prices_history= run_one_simulation(investors, market)
        
        evolution.append((np.mean(list(stocks_prices_history[-1].values())) - np.mean(list(stocks_prices_history[0].values())))/np.mean(list(stocks_prices_history[0].values())))
        
        money_of_each_investors = calculate_heritage_of_investors(investors,stocks_prices_history[-1]) 
        
        results.append(money_of_each_investors)
        
    print(f"crescimento das média das ações: {np.mean(evolution)*100}%\ndesvio padrão do crescimento: {np.std(evolution)*100}%")
    
    return results

def save_results_in_resultsfile(results):
    with open("results_file.txt", 'w') as file:
        header =  ",".join(f"investor {i}" for i in range(len(results[0])))
        file.write("simulation,"+header + "\n")
        for simulation , result in enumerate(results):
            line = ",".join(f"{value:.6f}" for value in result)
            file.write(f"{simulation+1}," + line + "\n")
           
def main():
    markets = generate_markets()
    estrategies = generate_estrategies() 
    results = run_all_simulations(markets,estrategies)
    save_results_in_resultsfile(results)
    show_statistics(results)
    
if __name__ == '__main__':
    main()