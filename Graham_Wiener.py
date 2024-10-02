#Definição das funções
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


class Investidores:
    def __init__(self, numero_investidores, recurso_inicial,limiar_min,ponto_intermediario,limiar_max,mercado,n_acao_alterada_por_iteracao, max_ativos_diferentes, numero_passos ):
        self.recurso_inicial = recurso_inicial
        self.numero_de_investidores = numero_investidores
        self.array_min = np.linspace(limiar_min, ponto_intermediario, self.numero_de_investidores)  # De limiar_min até o ponto intermediário
        #self.array_max = np.linspace(ponto_intermediario, limiar_max, numero_de_investidores)  # Do ponto intermediário até limiar_max
        self.array_max =np.full(self.numero_de_investidores, ponto_intermediario)
        self.investidores = np.array([[self.array_min[i], self.array_max[i]] for i in range(self.numero_de_investidores)])



        self.n_acao_alterada_por_iteracao = n_acao_alterada_por_iteracao
        self.max_ativos_diferentes = max_ativos_diferentes
        self.numero_passos = numero_passos
        


        self.mercado = mercado
    
        self.resultado_investidor_i = np.full(self.numero_de_investidores, self.recurso_inicial)
        self.carteira_investidor_i = np.zeros((self.numero_de_investidores, self.mercado.numero_ativos))

    def visualizar_resultado_investidores(self,array_limiar,resultado_investidor_i,titulo):
        plt.plot(array_limiar,resultado_investidor_i )
        plt.title('Simulação de Preço de Ativo Ajustado por Graham (GBM):'+titulo)
        plt.xlabel('Graham MIN')
        plt.ylabel('Resultado')
        plt.show()

    def visualizar_resultado_investidores_de_uma_so_vez(self,x, *arrays, titulo="Gráfico de Resultados"):
        if not arrays:
            raise ValueError("É necessário passar pelo menos um array para plotar.")
        
        for i, array in enumerate(arrays):
            plt.plot(x, array, label=f'Array {i+1}')
        
        plt.title(titulo)
        plt.xlabel('Graham MIN')
        plt.ylabel('Resultado')
        plt.legend()  # Adiciona uma legenda para identificar cada linha
        plt.show()

    def visualizar_resultado_investidores_e_desvio_padrao(self,graham_min:list, means:list, stdv:list) -> None:
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

    def realizar_estrategia(self):
        n_acao_alterada_por_iteracao = self.n_acao_alterada_por_iteracao
        max_ativos_diferentes = self.max_ativos_diferentes
        numero_passos = self.numero_passos
        
        for passo in range(0,numero_passos):
            #     if passo % 6 == 0 and passo != 0:
            #         rebalancear()
            #     if passo % 12 == 0 and passo != 0:
            #         reajuste_graham()
            n_ativo = 0 # para saber qual ativo
            for ativo in self.mercado.ativos:
                if(n_ativo ==  self.mercado.numero_ativos):
                    continue
                preco = ativo[passo]
                gasto = preco*n_acao_alterada_por_iteracao
                valor_intrinseco = self.mercado.valores_intriseco[n_ativo]
                for i in range(self.numero_de_investidores):
                    limiar_min_i = self.investidores[i][0]
                    limiar_max_i = self.investidores[i][1]
                    numero_ativos_diferentes = np.count_nonzero(self.carteira_investidor_i[i])
                    if preco > valor_intrinseco*limiar_max_i and self.carteira_investidor_i[i][n_ativo] >=1:
                        self.resultado_investidor_i[i] += gasto
                        self.carteira_investidor_i[i][n_ativo] -= n_acao_alterada_por_iteracao
                    if numero_ativos_diferentes > max_ativos_diferentes and self.carteira_investidor_i[i][n_ativo] == 0:
                        continue
                    if preco < valor_intrinseco*limiar_min_i and self.resultado_investidor_i[i]>gasto :
                        self.resultado_investidor_i[i] -= gasto
                        self.carteira_investidor_i[i][n_ativo] += n_acao_alterada_por_iteracao
                    if passo == numero_passos-1:
                        self.resultado_investidor_i[i] += self.carteira_investidor_i[i][n_ativo] * preco
                n_ativo+=1
            
    def zerar_investidores(self,mercado):
        self.carteira_investidor_i = np.zeros((self.numero_de_investidores, self.mercado.numero_ativos))
        self.resultado_investidor_i = np.full(self.numero_de_investidores, self.recurso_inicial)
        self.mercado = mercado


class Mercado:

    def __init__(self, numero_ativos, valor_intriseco_base,periodo_tempo,passos,crescimento_esperado,volatibilidade):
        self.numero_ativos = numero_ativos

        self.T = periodo_tempo  # Período de tempo (5 anos)
        self.N = passos  # Número de passos (mês) 
        self.dt = self.T / self.N  # Intervalo de tempo
        self.time = np.linspace(0, self.T, self.N) #array com cada mês

        self.mu_base = crescimento_esperado
        self.sigma_base = volatibilidade
        
        self.ativos = []
    

    def calcular_valor_intriseco_aleatorio(self):
        # self.valores_intriseco = np.random.standard_normal(size=self.numero_ativos)
        # self.valores_intriseco = self.valores_intriseco * self.valores_intriseco_base
        self.valores_intriseco = [np.random.uniform(1e+2, 1e+3) for _ in range(self.numero_ativos)]
    
    def calcular_valor_inicial(self,valor_intriseco):
        normal = np.random.normal(1,0.5/3)
        valor_inicial = normal* valor_intriseco
        return valor_inicial


    def visualizar_ativos(self):
        for i in range(0,self.numero_ativos):
            ativo = self.ativos[i]
            plt.plot(self.time, ativo.copy())
            plt.title('Simulação de Preço de Ativo Ajustado por Graham (GBM)')
            plt.xlabel('Tempo (anos)')
            plt.ylabel('Preço do Ativo')
            plt.show()

    def visualizar_mercado(self):
        for i in range(0,self.numero_ativos):
            ativo = self.ativos[i]
            plt.plot(self.time, ativo.copy())
        plt.title('Simulação de Preço de Ativo Ajustado por Graham (GBM)')
        plt.xlabel('Tempo (anos)')
        plt.ylabel('Preço do Ativo')
        plt.show()

    # Função para calcular a margem de segurança
    def calcular_margem_de_seguranca(self,valor_intrinseco,preco_mercado):
         return (valor_intrinseco - preco_mercado) / valor_intrinseco

    # Função para ajustar o retorno esperado baseado no valor intrínseco
    def ajustar_mu(self,preco_mercado, valor_intrinseco, mu_base):
        margem_de_seguranca = self.calcular_margem_de_seguranca(valor_intrinseco,preco_mercado)
        return mu_base * (1 + margem_de_seguranca)
    
    def criar_mercado(self):

        
        self.calcular_valor_intriseco_aleatorio()
        for valor_intrinseco in self.valores_intriseco:
            preco_inicial = self.calcular_valor_inicial(valor_intrinseco)
            mu = self.ajustar_mu(preco_inicial, valor_intrinseco, self.mu_base)
            sigma = self.sigma_base
            W = np.random.standard_normal(size=self.N)
            W = np.cumsum(W.copy()) * np.sqrt(self.dt) 
            
            
            ativo = preco_inicial * np.exp((mu - 0.5 * sigma**2) * self.time.copy() + sigma * W.copy()) # para o caso de achar que esquecemos o sqrt(t), olha o W mais em cima
            self.ativos.append(ativo)
        # self.visualizar_mercado()

    def zerar_mercado(self):
        self.ativos = []


class Resultados:
    def __init__(self, mercado,investidores,numero_de_simulacoes):
        self.mercado = mercado
        self.investidores = investidores
        self.numero_de_simulacoes = numero_de_simulacoes
        
    
        
    def run(self,seed_base):
        numero_de_simulacoes = self.numero_de_simulacoes
        numero_de_investidores = self.investidores.numero_de_investidores
        self.resultados_investidor_por_simulacao = [[0 for _ in range(numero_de_simulacoes)] for _ in range(numero_de_investidores)]
        for j in range(numero_de_simulacoes):
            seed = seed_base  + j
            np.random.seed(seed)
            self.mercado.criar_mercado()
            self.investidores.realizar_estrategia()
            for i in range(numero_de_investidores):
                resultado_investidor = self.investidores.resultado_investidor_i[i]
                self.resultados_investidor_por_simulacao[i][j] = resultado_investidor
            self.mercado.zerar_mercado()
            self.investidores.zerar_investidores(self.mercado)
        self.visualizar_resultado_simulacao()

    def calcular_int_confianca(self,results,confidence_level=0.95):
        mean_value = np.mean(results)
        std_err = stats.sem(results) 
        alpha = 1 - confidence_level
        t_value = stats.t.ppf(1 - alpha/2, df=len(results)-1)
        margin_of_error = t_value * std_err

        confidence_interval = (mean_value - margin_of_error, mean_value + margin_of_error)
        return confidence_interval
    
    def visualizar_int_confianca(self,array_min,confidence_intervals,media):
        # Convertendo o intervalo de confiança em arrays para facilitar o plot
        lower_bounds = [ci[0] for ci in confidence_intervals]
        upper_bounds = [ci[1] for ci in confidence_intervals]

        # Plotando os resultados
        plt.figure(figsize=(10, 6))
        plt.plot(array_min,media, label='Valor Médio dos Investidores', color='blue', marker='o')
        plt.fill_between(array_min, lower_bounds, upper_bounds, color='lightblue', alpha=0.5, label='Intervalo de Confiança (95%)')
        plt.title('Valor Médio e Intervalo de Confiança dos Investidores')
        plt.xlabel('Graham MIN')
        plt.ylabel('Valor Final (reais)')
        plt.axhline(y=self.investidores.recurso_inicial, color='red', linestyle='--', label='Investimento Inicial')
        plt.legend()
        plt.grid()
        plt.show()
    

    
    def visualizar_resultado_simulacao(self):
        numero_de_investidores = self.investidores.numero_de_investidores
        array_min = self.investidores.array_min
        media_investidor_simulacao = []
        desvio_padrao_investidor = []
        coeficiente_variacao_investidor = []
        variancia_investidor = []
        media_investidor_simulacaor_relativizado = []
        max_value_investidor = []
        min_value_investidor = []
        n_lucro_investidor = []
        intervalo_confianca_investidor = []

        desvio_padrao_investidor_relativizado = []

        crescimento_mercado = (1+self.mercado.mu_base)**(self.mercado.T)

        for i in range(0,numero_de_investidores):
            resultado_investidor = self.resultados_investidor_por_simulacao[i]
            
            media = sum(resultado_investidor) / len(resultado_investidor)
            
            desvio_padrao = np.std(resultado_investidor)
            
            variancia = np.var(resultado_investidor)
            coeficiente_variacao  = (desvio_padrao / media) * 100 

            media_investidor_simulacao.append( media  )
            desvio_padrao_investidor.append( desvio_padrao )
            variancia_investidor.append(variancia)
            coeficiente_variacao_investidor.append(coeficiente_variacao )

            resultados = np.array(self.resultados_investidor_por_simulacao[i])
            recurso_inicial = self.investidores.recurso_inicial
            resultado_investidor_relativizado = resultados / recurso_inicial
            media_relativizado = media/self.investidores.recurso_inicial
            desvio_padrao_relativizado = np.std(resultado_investidor_relativizado)
            media_investidor_simulacaor_relativizado.append( media_relativizado  )
            desvio_padrao_investidor_relativizado.append( desvio_padrao_relativizado )


            maior_valor = max(resultado_investidor)
            menor_valor = min(resultado_investidor)

            valores_maiores_que_crescimento_mercado= [valor for valor in resultado_investidor if valor > (self.investidores.recurso_inicial*crescimento_mercado)]
            n_valores_maiores_que_crescimento_mercado = len(valores_maiores_que_crescimento_mercado)
            max_value_investidor.append(maior_valor)
            min_value_investidor.append( menor_valor )
            n_lucro_investidor.append(n_valores_maiores_que_crescimento_mercado  )


            int_confianca = self.calcular_int_confianca(resultado_investidor)
            intervalo_confianca_investidor.append(int_confianca)

        
        # self.investidores.visualizar_resultado_investidores(array_min,media_investidor_simulacao,"media")
        # self.investidores.visualizar_resultado_investidores(array_min,desvio_padrao_investidor,"desvio padrao")
        # self.investidores.visualizar_resultado_investidores(array_min,variancia_investidor,"variancia")
        # self.investidores.visualizar_resultado_investidores(array_min,coeficiente_variacao_investidor,"coeficiente de variacao")

        self.investidores.visualizar_resultado_investidores_de_uma_so_vez(array_min,media_investidor_simulacao,desvio_padrao_investidor,coeficiente_variacao_investidor)

        self.investidores.visualizar_resultado_investidores_de_uma_so_vez(array_min,max_value_investidor,min_value_investidor)

        self.investidores.visualizar_resultado_investidores_e_desvio_padrao(array_min,media_investidor_simulacaor_relativizado,desvio_padrao_investidor_relativizado)
        self.investidores.visualizar_resultado_investidores(array_min,n_lucro_investidor,"N > 1.3*RI")
        self.visualizar_int_confianca(array_min,intervalo_confianca_investidor,media_investidor_simulacao)
        
        


def main():
    #Simulacao
    numero_de_simulacoes = 300
    seed_base =42

    #graham
    valor_intriseco_base = 50
    limiar_min = 0.4 #limite inferior
    limiar_max = 1.1 #limite superior
    ponto_intermediario = 0.9 # meio termo

    #wiener
    mu_base = 0.05  # Retorno base (média histórica)
    sigma_base = 0.03  # Volatilidade base

    #mercado
    numero_de_ativos = 10

    #investidores 
    numero_de_investidores = 150
    recurso_inicial = 1000
    n_acao_alterada_por_iteracao = 1    
    max_ativos_diferentes = 10

    # Simulação do Movimento Browniano Geométrico (GBM)
    T = 5  # Período de tempo (5 anos)
    N = 5*12  # Número de passos (mês) 
    dt = T / N  # Intervalo de tempo

    mercado = Mercado(
        numero_ativos=numero_de_ativos,
        passos=N,
        valor_intriseco_base=valor_intriseco_base,
        periodo_tempo=T,
        crescimento_esperado=mu_base,
        volatibilidade=sigma_base
        )
    investidores = Investidores(numero_investidores=numero_de_investidores,
                                recurso_inicial=recurso_inicial,
                                limiar_min=limiar_min,
                                ponto_intermediario=ponto_intermediario,
                                limiar_max=limiar_max,
                                mercado=mercado,
                                n_acao_alterada_por_iteracao=n_acao_alterada_por_iteracao,
                                max_ativos_diferentes=max_ativos_diferentes,
                                numero_passos=N
                                )
    
    simulacao = Resultados(
                            mercado=mercado,
                            investidores=investidores,
                            numero_de_simulacoes=numero_de_simulacoes
                           )

    simulacao.run(seed_base= seed_base)


if __name__ == "__main__":
    main()
        

