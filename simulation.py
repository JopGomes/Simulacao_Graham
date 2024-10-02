import random
from investidor import Investor
from mercados import Market
import matplotlib.pyplot as plt
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
    smallest_sell_limit = 0.95
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
    #print(estragies[88])
    #print(estragies[99])
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

def plot_graphic(lista:list[dict]) -> None:
    x = np.arange(NUMBER_OF_MONTHS)
    for i in range(NUMBER_OF_STOCKS):
        stock_i = []
        for stock_month_j in lista:
            stock_i.append(stock_month_j[i])
        plt.plot(x,stock_i,label=f'ação: {i}')
    
    plt.title(F'Gráfico das {NUMBER_OF_STOCKS} ações')
    plt.xlabel('mês')
    plt.ylabel('preço')

    plt.legend()

    plt.grid()  
    plt.show()
        
def calculate_heritage_of_investors(investors:list[Investor],stocks_prices:dict) -> list[float]:
    result = []   
    for investor in investors:
        result.append(investor.get_heritage(stocks_prices)) 
    return result   
        
def run_one_simulation(investors:list[Investor], market:Market) -> list[dict]:
    real_stock_prices = []
    fair_stock_prices = []

    for month in range(0,NUMBER_OF_MONTHS):
        fair_stock_prices.append(market.get_fair_stock_prices())
        real_stock_prices.append(market.get_real_stock_prices())
        
        for investor in investors:
            investor.search_stock_to_sell(real_stock_prices[month], fair_stock_prices[month])
            investor.search_stock_to_buy(real_stock_prices[month], fair_stock_prices[month])
            
            if (month + 1) % 6 == 0:
                investor.rebalance_wallet(real_stock_prices[month])
            
        if (month + 1) % 12 == 0:
            market.update_fair_stock_prices()
        
        market.update_real_stock_prices()
    
    #plot_graphic(real_stock_prices)
    #plot_graphic(lista_fair)
    
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
           
def show_statistics(results:list[float]) -> None:
    number_of_estrategies = len(results[0])
    mean = []
    standart_deviation = []
    for i in range(number_of_estrategies):
        investor_with_estrategy_i = []
        
        for simulation_result in results:
            money_of_investor_with_estrategy_i = simulation_result[i]
            investor_with_estrategy_i.append(money_of_investor_with_estrategy_i)
            
        mean.append(round(np.mean(investor_with_estrategy_i) ,6))    
        standart_deviation.append(round(np.std(investor_with_estrategy_i),6))
        #print(f"variação média:{round(np.mean(investor_with_estrategy_i),6)}, desv padrão:{round(np.std(investor_with_estrategy_i),6)}")
        
    show_graphics_of_results(mean,standart_deviation)
    

def show_graphics_of_results(means:list, stdv:list) -> None:
    x = np.arange(len(means))
    
    # Criando gráfico de barras
    plt.bar(x, means,yerr = stdv, color='skyblue', alpha=0.7)
    
    # Definindo título e rótulos dos eixos
    plt.title(f'Gráfico das {len(means)} estratégias')
    plt.xlabel('Estratégia')
    plt.ylabel('Ganho')
    
    # Adicionando uma grade ao gráfico
    plt.grid(True)
    
    # Exibindo o gráfico
    plt.show()

def main():
    markets = generate_markets()
    estrategies = generate_estrategies() 
    results = run_all_simulations(markets,estrategies)
    show_statistics(results)
    
if __name__ == '__main__':
    main()