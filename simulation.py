"""
    CEN0366 

    Modelo Computacional para predição do efeito da temperatura no crescimento populacional de insetos

    Autores: Bruno Scatena Gatti, Carolina Pacchioni Monteiro, Tiago Estevam Corrêa

"""

import sys
import matplotlib.pyplot as plt
import math
import random

def simular_crescimento(dados, N, tempo_de_simulacao = 30, temperatura = 0, linhagem = ""):
    # pegar o valor de r da tabela e a população inicial, iniciar variáveis (armazenar em variáveis os resultados que queremos)
    resultados = [] # criar lista dos resultados
    rs = [] # criar lista dos valores de r
    temperatura = int(temperatura) # transformar temperatura de string para inteiro
    temps = [] #criar lista
    for temp in dados[linhagem]:
        temps.append(int(temp)) # adicionar os valores de temperatura na lista
    r = float(dados[linhagem][str(temperatura)])  # pegar o valor de r
    pop = int(N) # iniciar a população
    resultados.append(pop) # adicionar a população inicial aos resultados
    rs.append(r) # adicionar o valor de r aos resultados
    ts = [temperatura] # adicionar a temperatura aos resultados


    for t in range(tempo_de_simulacao):        

        # escolhendo uma nova temperatura e calculando o novo valor de r
        # o r será considerado como linear entre os valores de temperatura, logo, o valor de r será calculado por interpolação linear
        # a temperatura será truncada para os valores de temperatura fornecidos nos dados

        new_temp = temperatura + random.uniform(-1,1) # gerar um novo valor de temperatura
        if new_temp > temps[-1]: # se a temperatura for maior que a máxima
            temperatura = temps[-1]
        elif new_temp < temps[0]: # se a temperatura for menor que a mínima
            temperatura = temps[0]
        else: # se a temperatura estiver dentro do intervalo
            temperatura = new_temp
        
        if temperatura < temps[1]: # se a temperatura for menor que a do meio
            new_r = (temps[1] - temperatura) * ((float(dados[linhagem][str(temps[1])]) - float(dados[linhagem][str(temps[0])])) / (temps[1] - temps[0]) + float(dados[linhagem][str(temps[0])]))
        elif temperatura > temps[1]: # se a temperatura for maior que a do meio
            new_r = (temperatura - temps[1]) * ((float(dados[linhagem][str(temps[2])]) - float(dados[linhagem][str(temps[1])])) / (temps[2] - temps[1]) + float(dados[linhagem][str(temps[1])]))
        else:
            new_r = float(dados[linhagem][str(temps[1])])
        
        r = new_r

        var_n = r * pop # calcular a variação na população
        pop += var_n # atualizar o número populacional
        resultados.append(pop) # adicionar o novo número populacional aos resultados
        rs.append(r) # adicionar o novo valor de r aos resultados
        ts.append(temperatura) # adicionar a nova temperatura aos resultados
     
    with open("out.txt", "w") as file: # salvando os resultados em um arquivo txt
        file.write("Tempo\tPopulação\tR\tTemps\n")
        for t in range(len(resultados)):
            file.write(str(t) + "\t" + str(resultados[t]) + "\t" + str(rs[t]) + "\t" + str(ts[t]) + "\n")
    return resultados # retornar os resultados

def graph_results(resultados):
    # plotar os resultados
    plot = plt.plot(resultados)

    # adicionar título ao gráfico
    plt.title("Crescimento populacional")
    # adicionar rótulos aos eixos
    plt.xlabel("Tempo (dias)")
    plt.ylabel("População")
    # salvar o gráfico
    plt.savefig("resultados.png")

def main(): # função principal
    arquivo = input("Arquivo de dados: ") # pegar o nome do arquivo de dados
    
    linhagens = {} # criar um dicionário vazio para armazenar os dados da tabela
    
    try:    # o arquivo deve existir
        with open(arquivo, "r") as file: # abrir o arquivo de dados            
            try: # a primeira linha informa temperatura
                temperaturas = file.readline().split() # pegar a linha com as temperaturas
                for temperatura in temperaturas: # verificar se as temperaturas são números
                    float(temperatura)
            except(ValueError):
                print("A primeira linha deve conter apenas números, representando as temperaturas")
                sys.exit()
            
        
            for line in file: 
                dados = line.split() # separar os dados da linha
                try: # a primeira coluna é uma string e informa linhagem, as próximas colunas são float
                    float(dados[1]) # verificar se o segundo item é um número
                except(ValueError):
                    print("A primeira coluna deve ser uma string e as próximas colunas devem ser números")
                    sys.exit()

                
                linhagens[dados[0]] = {} 

                for temperatura in temperaturas: 
                    linhagens[dados[0]][temperatura] = dados[temperaturas.index(temperatura) + 1] # armazenar os dados no dicionário

        
                try: # todas as próximas linhas devem ter o mesmo número de itens
                    if len(dados) != len(temperaturas) + 1:
                        raise ValueError
                except(ValueError):
                    print("Todas as linhas devem ter o mesmo número de itens")
                    sys.exit()

    except:
        print("O arquivo não existe ou não pode ser lido")
        sys.exit()
    
    try: # verificar se os dados são válidos
        tempo = int(input("Duração da simulação: ")) # pegar a duração da simulação no terminal
        
        N_inicial = int(input("População inicial: ")) # pegar a população inicial no terminal
    except(ValueError):
        print("O tempo e o N inicial devem ser inteiros")
        sys.exit()
    linhagem = input("Linhagem (Opções " + ", ".join(linhagens.keys()) + "): ") # pegar a linhagem no terminal

    temperatura = input("Temperatura (Opções " + ", ".join(temperaturas) + "): ") # pegar a temperatura no terminal
    
    try:
        if not linhagem in linhagens.keys(): # a linhagem deve ser uma das fornecidas nos dados
            print("A linhagem deve ser uma das fornecidas nos dados")
            raise ValueError
        if not temperatura in temperaturas: # a temperatura deve ser uma das fornecidas nos dados
            print("A temperatura deve ser uma das fornecidas nos dados")
            raise ValueError
        if not N_inicial > 0: # o N inicial deve ser inteiro e maior que zero
            print("O N inicial deve ser maior que zero")
            raise ValueError
        if not N_inicial < 1000000: # o N inicial deve ter limite de 1 milhão
            print("O N inicial deve ser menor que 1 milhão")
            raise ValueError
        if not tempo > 0: # o tempo deve ser inteiro e maior que zero
            print("O tempo deve ser maior que zero")
            raise ValueError
        if not tempo < 200: # o tempo deve ter limite de 200 dias
            print("O tempo deve ser menor que 200 dias")
            raise ValueError
        
    except(ValueError):
        sys.exit()


    # chamar a função simulate_growth
    resultados = simular_crescimento(linhagens, N_inicial, tempo, temperatura, linhagem = linhagem)
    
    # chamar a função graph_results
    graph_results(resultados)

if __name__ == "__main__": # se o programa for executado diretamente
    main() # chamar a função main

