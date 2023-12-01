"""
    CEN0366 

    Modelo Computacional para predição do efeito da temperatura no crescimento populacional de insetos

    Autores: Bruno Scatena Gatti, Carolina Pacchioni Monteiro, Tiago Estevam Corrêa

"""

import sys
import random
import argparse
from typing import List
import matplotlib.pyplot as plt

def simular_crescimento(dados, N, tempo_de_simulacao: int = 30, temperatura: int = 0, linhagem: str = "", var_temp: List[int] = [-1, 1]) -> list:
    try:
        if tempo_de_simulacao <= 0:
            raise ValueError("Este método precisa que o tempo seja maior que zero")
        if not N > 0:
            raise ValueError("Este método precisa que a população inicial seja maior que zero")
        if not linhagem in dados.keys():
            raise ValueError("Este método precisa que a linhagem seja uma das fornecidas nos dados")
        if not temperatura in dados[linhagem].keys():
            raise ValueError("Este método precisa que a temperatura inicial seja uma das fornecidas nos dados")
        if len(var_temp) != 2:
            raise ValueError("Este método precisa que a variação de temperatura seja uma lista com dois valores")
    except(ValueError):
        sys.exit()
    
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

        new_temp = temperatura + random.uniform(var_temp[0],var_temp[1]) # gerar um novo valor de temperatura
        if new_temp > temps[-1]: # se a temperatura for maior que a máxima
            temperatura = temps[-1]
        elif new_temp < temps[0]: # se a temperatura for menor que a mínima
            temperatura = temps[0]
        else: # se a temperatura estiver dentro do intervalo
            temperatura = new_temp
        
        # novo r = r_menor + (r2 - r1) * (t - t1) / (t2 - t1)
        if temperatura < temps[1]: # se a temperatura for menor que a do meio
            new_r = float(dados[linhagem][str(temps[0])]) + (float(dados[linhagem][str(temps[1])]) - float(dados[linhagem][str(temps[0])])) * (temperatura - temps[0]) / (temps[1] - temps[0])
        elif temperatura > temps[1]: # se a temperatura for maior que a do meio
            new_r = float(dados[linhagem][str(temps[1])]) + (float(dados[linhagem][str(temps[2])]) - float(dados[linhagem][str(temps[1])])) * (temperatura - temps[1]) / (temps[2] - temps[1])
        else:
            new_r = float(dados[linhagem][str(temps[1])])
        
        r = new_r

        var_n = r * pop # calcular a variação na população
        pop += var_n # atualizar o número populacional
        resultados.append(pop) # adicionar o novo número populacional aos resultados
        rs.append(r) # adicionar o novo valor de r aos resultados
        ts.append(temperatura) # adicionar a nova temperatura aos resultados

    return resultados, rs, ts # retornar os resultados

def graph_results(dados, title, yLabel, name = "out.png"):
    # plotar os resultados
    plot = plt.plot(dados)

    # adicionar título ao gráfico
    plt.title(title)
    # adicionar rótulos aos eixos
    plt.xlabel("Tempo (dias)")
    plt.ylabel(yLabel)
    # salvar o gráfico
    plt.savefig(name)
    # fechar o gráfico
    plt.close()

def main(): # função principal

    # inputs pelo argparse
    ajuda = """Intruções de uso: \npython simulation.py -i <arquivo> -t <tempo> -n <população inicial> -l <linhagem> -T <temperatura> --var_inf <limite inferior de variação da temperatura> --var_sup <limite superior de variação da temperatura>
OU apenas python simulation.py. Nesse caso, os dados serão solicitados pelo terminal.
   Arquivo de dados deve conter: Primeira linha com as temperaturas, as próximas linhas com a primeira coluna sendo a linhagem e as próximas colunas sendo os valores de r para cada temperatura
   Tempo de simulação deve ser um inteiro maior que zero
   População inicial deve ser um inteiro maior que zero e menor que 1 milhão
   Linhagem deve ser uma das fornecidas nos dados
   Temperatura deve ser uma das fornecidas nos dados
   Opcional: variação da temperatura deve ser uma lista com dois valores, o primeiro sendo o limite inferior e o segundo sendo o limite superior de variação da temperatura"""
    parser = argparse.ArgumentParser(description=ajuda, formatter_class=argparse.RawTextHelpFormatter)
    # formatter_class=argparse.RawTextHelpFormatter -> para que a ajuda seja exibida corretamente (com quebra de linhas)

    # --arquivo ou -i: arquivo de dados
    parser.add_argument('--arquivo', '-i', type=str, help='Arquivo de dados')
    # --tempo ou -t: tempo de simulação
    parser.add_argument('--tempo', '-t', type=int, help='Duração da simulação (em dias) [1, 200]]')
    # --pop ou -n: população inicial
    parser.add_argument('--pop', '-n', type=int, help='População inicial [1, 1000000]]')
    # --linhagem ou -l: linhagem
    parser.add_argument('--linhagem', '-l', type=str, help='Linhagem, entre as fornecidas nos dados')
    # --temperatura ou -T: temperatura
    parser.add_argument('--temperatura', '-T', type=str, help='Temperatura, entre as fornecidas nos dados')
    # --var_inf: limite inferior de variação da temperatura
    parser.add_argument('--var_inf', '-v_i', type=int, help='Opc: Limite inferior de variação da temperatura (padrão: -1)')
    # --var_sup: limite superior de variação da temperatura
    parser.add_argument('--var_sup', '-v_s', type=int, help='Opc: Limite superior de variação da temperatura (padrão: 1)')
    args = parser.parse_args()

    # os dados podem ser fornecidos pelo terminal ou pelo argparse
    if not args.arquivo:
        arquivo = input("Arquivo de dados: ") # pegar o nome do arquivo de dados
    else:
        arquivo = args.arquivo
    
    linhagens = {} # criar um dicionário vazio para armazenar os dados da tabela
    
    # ler o arquivo de dados e armazenar os dados no dicionário
    try: # o arquivo deve existir
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
    except FileNotFoundError:
        print("O arquivo não existe ou não pode ser lido")
        sys.exit()

    if not args.tempo: # pegar o tempo de simulação no terminal, caso não tenha sido fornecido pelo argparse
        try: # verificar se os dados são válidos
            tempo = int(input("Duração da simulação: ")) # pegar a duração da simulação no terminal
        except ValueError:
            print("O tempo e o N inicial devem ser inteiros")
            sys.exit()
    else:
        tempo = args.tempo

    if not args.pop: # pegar a população inicial no terminal, caso não tenha sido fornecida pelo argparse
        try: # verificar se os dados são válidos
            N_inicial = int(input("População inicial: ")) # pegar a população inicial no terminal
        except ValueError:
            print("O tempo e o N inicial devem ser inteiros")
            sys.exit()
    else:
        N_inicial = args.pop

    if not args.linhagem: # pegar a linhagem no terminal, caso não tenha sido fornecida pelo argparse
        linhagem = input("Linhagem (Opções " + ", ".join(linhagens.keys()) + "): ") # pegar a linhagem no terminal
    else:
        linhagem = args.linhagem

    if not args.temperatura: # pegar a temperatura no terminal, caso não tenha sido fornecida pelo argparse
        temperatura = input("Temperatura (Opções " + ", ".join(temperaturas) + "): ") # pegar a temperatura no terminal
    else:
        temperatura = args.temperatura
    
    # pegar a variação da temperatura no terminal, caso não tenha sido fornecida pelo argparse
    if not args.var_inf:
        var_temps = input("Opcional: variação da temperatura, separadas por vírgula (Vazio = -1, 1): ") # pegar a variação da temperatura no terminal
        if not var_temps: # se não foi fornecida uma variação da temperatura, usar os valores padrão
            var_inf = -1
            var_sup = 1
        else:
            var_temps = var_temps.strip(" ").split(",")

            if not isinstance(var_temps, list) or len(var_temps) != 2:
                # caso sejam fornecidos valores inválidos, usar os valores padrão e avisar
                print("A variação da temperatura deve ser uma lista com dois valores. Ex: -1, 1. Usando os valores padrão")
                var_inf = -1
                var_sup = 1
            else:
                var_inf = var_temps[0]
                var_sup = var_temps[1]
                # se algum dos valores não for fornecido, usar os valores padrão
                if var_inf == "":
                    var_inf = -1
                if var_sup == "":
                    var_sup = 1
    else: # se a variação da temperatura foi fornecida pelo argparse
        var_inf = args.var_inf
        var_sup = args.var_sup
    
    # Testes de validação dos dados
    try:
        if not linhagem in linhagens: # a linhagem deve ser uma das fornecidas nos dados
            print("A linhagem deve ser uma das fornecidas nos dados")
            raise ValueError
        if not temperatura in temperaturas: # a temperatura deve ser uma das fornecidas nos dados
            print("A temperatura deve ser uma das fornecidas nos dados")
            raise ValueError
        if N_inicial <= 0: # o N inicial deve ser inteiro e maior que zero
            print("O N inicial deve ser maior que zero")
            raise ValueError
        if N_inicial > 1000000: # o N inicial não pode ser maior que 1 milhão
            print("O N inicial deve ser menor que 1 milhão")
            raise ValueError
        if tempo <= 0: # o tempo deve ser inteiro e maior que zero
            print("O tempo deve ser maior que zero")
            raise ValueError
        if tempo >= 200: # o tempo deve ter limite de 200 dias
            print("O tempo deve ser menor que 200 dias")
            raise ValueError
        var_inf = int(var_inf) # a variação da temperatura deve ser inteira
        var_sup = int(var_sup) # a variação da temperatura deve ser inteira

    except ValueError as e:
        print(e)
        sys.exit()

    # chamar a função simulate_growth
    resultados, resultado_r, resultado_t = simular_crescimento(linhagens, N_inicial, tempo, temperatura, linhagem = linhagem, var_temp = [var_inf, var_sup])
    
    # chamar a função graph_results para plotar os resultados
    graph_results(resultados, "Crescimento populacional da linhagem " + linhagem + " a temperatura inicial " + temperatura + "°C", "População", name = "resultados.png")
    graph_results(resultado_r, "Variação de r da linhagem por dia", "r", name = "out_r.png")
    graph_results(resultado_t, "Variação de temperatura por dia", "Temperatura (°C)", name = "out_t.png")

    # salvar os resultados em um arquivo
     
    with open("out.txt", "w") as file: # salvando os resultados em um arquivo txt
        file.write("Tempo\tPopulação\tR\tTemps\n")
        for t in range(len(resultados)):
            file.write(str(t) + "\t" + str(resultados[t]) + "\t" + str(resultado_r[t]) + "\t" + str(resultado_t[t]) + "\n")


if __name__ == "__main__": # se o programa for executado diretamente
    main() # chamar a função main

