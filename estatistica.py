import matplotlib.pyplot as plt
import numpy as np

def show_statistics(results:list[float]) -> None:
    number_of_estrategies = len(results[0])
    means = []
    standart_deviations = []
    
    for i in range(number_of_estrategies):
        investor_with_estrategy_i = []
        
        for simulation_result in results:
            money_of_investor_with_estrategy_i = simulation_result[i]
            investor_with_estrategy_i.append(money_of_investor_with_estrategy_i)
            
        means.append(round(np.mean(investor_with_estrategy_i) ,6))    
        standart_deviations.append(round(np.std(investor_with_estrategy_i),6))
    
    max_return = max(means)
    max_return_index = means.index(max_return)
    print(f"media:{max_return}, desvio padrao:{standart_deviations[max_return_index]}")
    
    show_graphics_of_results(means,standart_deviations)

def show_graphics_of_results(means:list, stdv:list) -> None:
    x = np.arange(len(means))

    plt.bar(x, means,yerr = stdv, color='skyblue', alpha=0.7)
    
    plt.title(f'Gráfico das {len(means)} estratégias')
    plt.xlabel('Estratégia')
    plt.ylabel('Ganho')
    
    plt.grid(True)
    plt.show()
    
def get_data_from_resultsfile() -> list[float]:
    results = []
    with open("results_file.txt", 'r') as file:
        next(file)
        for line in file:
            values = line.strip("\n").split(',')
            values = values[1:]
            results.append([float(value) for value in values])
    return results
    
if __name__ == "__main__":
    results = get_data_from_resultsfile()
    show_statistics(results)