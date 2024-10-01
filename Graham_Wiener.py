#Definição das funções
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular o valor intrínseco usando a fórmula de Graham
def calcular_valor_intrinseco(LPA, VPA):
    return np.sqrt(22.5 * LPA * VPA)



class Investidores:
    def __init__(self, numero_investidores, recurso_inicial,limiar_min,ponto_intermediario,limiar_max,mercado,n_acao_alterada_por_iteracao, max_ativos_diferentes, numero_passos ):
        self.recurso_inicial = recurso_inicial
        self.numero_de_investidores = numero_investidores
        self.array_min = np.linspace(limiar_min, ponto_intermediario, self.numero_de_investidores)  # De limiar_min até o ponto intermediário
        #self.array_max = np.linspace(ponto_intermediario, limiar_max, numero_de_investidores)  # Do ponto intermediário até limiar_max
        self.array_max =np.full(self.numero_de_investidores, ponto_intermediario)
        self.investidores = np.array([[self.array_min[i], self.array_max[i]] for i in range(self.numero_de_investidores)])


        self.resultado_investidor_i = np.full(self.numero_de_investidores, self.recurso_inicial)

        self.n_acao_alterada_por_iteracao = n_acao_alterada_por_iteracao
        self.max_ativos_diferentes = max_ativos_diferentes
        self.numero_passos = numero_passos
        


        self.mercado = mercado
    
        self.carteira_investidor_i = np.zeros((self.numero_de_investidores, self.mercado.numero_ativos))

    def visualizar_resultado_investidores(self,array_limiar,resultado_investidor_i):
        plt.plot(array_limiar,resultado_investidor_i )
        plt.title('Simulação de Preço de Ativo Ajustado por Graham (GBM)')
        plt.xlabel('Graham MIN')
        plt.ylabel('Resultado')
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

        self.ativos = []
        self.calcular_valor_intriseco_aleatorio()
        for valor_intrinseco in self.valores_intriseco:
            mu = self.ajustar_mu(valor_intrinseco, valor_intrinseco, self.mu_base)
            sigma = self.sigma_base
            W = np.random.standard_normal(size=self.N)
            W = np.cumsum(W.copy()) * np.sqrt(self.dt) 
            
            preco_inicial = self.calcular_valor_inicial(valor_intrinseco)
            ativo = preco_inicial * np.exp((mu - 0.5 * sigma**2) * self.time.copy() + sigma * W.copy()) # para o caso de achar que esquecemos o sqrt(t), olha o W mais em cima
            self.ativos.append(ativo)
        self.visualizar_mercado()



class Resultados:
    def __init__(self, mercado,investidores):
        self.mercado = mercado
        self.investidores = investidores
        
    
    def run(self,numero_de_simulacoes,seed_base):

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
        self.visualizar_resultado_simulacao()

    

    
    def visualizar_resultado_simulacao(self):
        numero_de_investidores = self.investidores.numero_de_investidores
        array_min = self.investidores.array_min
        media_investidor_simulacao = []
        desvio_padrao_investidor = []
        coeficiente_variacao_investidor = []
        variancia_investidor = []
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
        
        self.investidores.visualizar_resultado_investidores(array_min,media_investidor_simulacao)
        self.investidores.visualizar_resultado_investidores(array_min,desvio_padrao_investidor)
        self.investidores.visualizar_resultado_investidores(array_min,variancia_investidor)
        self.investidores.visualizar_resultado_investidores(array_min,coeficiente_variacao_investidor)
        
        
        


def main():
    #Simulacao
    numero_de_simulacoes = 5
    seed_base =42

    #graham
    valor_intriseco_base = 50
    limiar_min = 0.5 #limite inferior
    limiar_max = 1.1 #limite superior
    ponto_intermediario = 1 # meio termo

    #wiener
    mu_base = 0.05  # Retorno base (média histórica)
    sigma_base = 0.5  # Volatilidade base

    #mercado
    numero_de_ativos = 10

    #investidores 
    numero_de_investidores = 100
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
    simulacao = Resultados(mercado=mercado,investidores=investidores)

    simulacao.run(numero_de_simulacoes=numero_de_simulacoes,
                  seed_base= seed_base
                  )


if __name__ == "__main__":
    main()
        

