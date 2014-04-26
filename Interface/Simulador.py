# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#a primeira função cria um dicionário onde cada cidade é um chave e os itens são listas formadas pelas frações de cortes, tois e negativações
#em cada uma. A lista ainda traz o total de contratos na cidade. O resultado terá mais ou menos esta cara: (cidade:[cortes da cidade/total de cortes,
#tois da cidade/total de tois, negativações da cidade/total de negativações, total de contratos da cidade]) Esta última informação será necessária
#para se calcular a quantidade de clientes em uma cidade que não foram especificados tendo esta ou aquela nota.
def criardicionariorateio(arquivo):
    import csv

    cidades = csv.reader(open(arquivo, "rb"))
    #este csv é formado por nove colunas: município, número do contrato, data de início do contrato, data do fim do contrato,
    #data de processo, data de corte,  data de toi,  data de reclamação e  data de negativação.
    global dicionariorateio
    dicionariorateio = {}
    totalcor = 0.0
    totaltoi = 0.0
    totalneg = 0.0
    for linha in cidades:
        if linha[0] != "":
            if linha[5] != "":
                totalcor += 1
            if linha[6] != "":
                totaltoi += 1
            if linha[8] != "":
                totalneg += 1
    cidades = csv.reader(open(arquivo, "rb"))
    for linha in cidades:
        if linha[0] != "":
            if dicionariorateio.has_key(linha[0]):
                if linha[5] != "":
                    dicionariorateio[linha[0]][0] += 1
                if linha[6] != "":
                    dicionariorateio[linha[0]][1] += 1
                if linha[8] != "":
                    dicionariorateio[linha[0]][2] += 1
                dicionariorateio[linha[0]][3] += 1
            else:
                dicionariorateio[linha[0]] = [0, 0, 0, 0]
    for chave in dicionariorateio:
        dicionariorateio[chave][0] = dicionariorateio[chave][0] / totalcor
        dicionariorateio[chave][1] = dicionariorateio[chave][1] / totaltoi
        dicionariorateio[chave][2] = dicionariorateio[chave][2] / totalneg


criardicionariorateio('tabelaparaosimulador.csv')
#após este comando, teremos o objeto global "dicionariorateio"

#a próxima função apenas lê o csv que o David gerou no R com os parâmetros a partir da Análise de Sobrevivência. A partir do arquivo,
#cria-se também um dicionário, novamente tendo o nome da cidade como chave. O valor é uma lista de nove números, com "alphas" para as
#seguintes situações: clientes em geral, clientes com corte, clientes com toi, clientes com negativação, clientes com corte e toi, 
# clientes com toi e negativação, clientes com corte e negativação, clientes com corte toi e negativação, clientes sem nota.
def criardicionarioalphas(arquivo):
    import csv

    indices = csv.reader(open(arquivo, "rb"))
    global dicionarioalphas
    dicionarioalphas = {}
    for linha in indices:
        dicionarioalphas[linha[1]] = []
        dicionarioalphas[linha[1]].append(linha[2])
        dicionarioalphas[linha[1]].append(linha[3])
        dicionarioalphas[linha[1]].append(linha[4])
        dicionarioalphas[linha[1]].append(linha[5])
        dicionarioalphas[linha[1]].append(linha[6])
        dicionarioalphas[linha[1]].append(linha[7])
        dicionarioalphas[linha[1]].append(linha[8])
        dicionarioalphas[linha[1]].append(linha[9])
        dicionarioalphas[linha[1]].append(linha[10])


criardicionarioalphas('alphas.csv')
#agora também teremos o objeto global "dicionarioalphas"

#bom... chegamos à parte mais difícil. A próxima função (cujo nome é tosco, eu sei) divide o total de cortes tois e negativações entre uma
#população de x pessoas. Os valores são encontrados com base em teoria de conjuntos e exprimem a provável média de distribuição que
#encontraríamos caso simulássemos muitas vezes. Os cálculos lidam explicitamente com uniões e interseções, o que pode poluir um pouco.
#Esta função ainda lida com outro problema: o caso de nosso usuário não informar a quantidade de notas. Quando isto acontecer,
#entenderemos que a parte da população "sem nota" seguirá o padrão geral (nosso alpha0, que vale para todo mundo). Já quando o sujeito informar
#todas as quantidades, então entenderemos que quem ficar sem nota estará, de fato, sem estas notas. Então usaremos o alpha de quem não
#tem notas.
#Sugiro experimentar esta função isoladamente. Ela deve ser acionada com os seguintes parâmetros: total de pessoas, cortes, TOIs e negativações.
#Ela retorna uma lista com nove valores inteiros. O primeiro é a quantidade de pessoas "genéricas", ou seja, aquelas que não sabemos
#que notas têm ou não. Sempre que o usuário informar todos os valores, este total será zero. Os demais valores da lista são os totais de
#pessoas que tiveram corte, toi, negativação, corte e toi, toi e negativação, corte e negativação, as três coisas e, finalmente, o total de pessoas
#que não teve qualquer destas notas. Este valor será zero quando o usuário não especificar quanto de cada nota teremos.
def dividindo(x, c=None, t=None, n=None):
    global listaquantidades
    if c != None and t != None and n != None:
        c = float(c)
        n = float(n)
        t = float(t)
        listaquantidades = [0, int(round(x * (c / x + (c * t * n / (x ** 3)) - (c * t / (x * x)) - (c * n / (x * x))))),
                            int(round(x * (t / x + (c * t * n / (x ** 3)) - (c * t / (x * x)) - (t * n / (x * x))))),
                            int(round(x * (n / x + (c * t * n / (x ** 3)) - (n * t / (x * x)) - (c * n / (x * x))))),
                            int(round(x * ((c * t / (x * x)) - (c * t * n / (x ** 3))))),
                            int(round(x * ((t * n / (x * x)) - (c * t * n / (x ** 3))))),
                            int(round(x * ((c * n / (x * x)) - (c * t * n / (x ** 3))))),
                            int(round(x * ((c * t * n / (x ** 3))))), int(round(x * (
            1 - c / x - n / x - t / x - (c * t * n / (x ** 3)) + (c * t / (x * x)) + (c * n / (x * x)) + (
            n * t / (x * x)))))]
    else:
        if c == None:
            c = 0
        if t == None:
            t = 0
        if n == None:
            n = 0
        c = float(c)
        n = float(n)
        t = float(t)
        listaquantidades = [int(round(x * (
        1 - c / x - n / x - t / x - (c * t * n / (x ** 3)) + (c * t / (x * x)) + (c * n / (x * x)) + (
        n * t / (x * x))))), int(round(x * (c / x + (c * t * n / (x ** 3)) - (c * t / (x * x)) - (c * n / (x * x))))),
                            int(round(x * (t / x + (c * t * n / (x ** 3)) - (c * t / (x * x)) - (t * n / (x * x))))),
                            int(round(x * (n / x + (c * t * n / (x ** 3)) - (n * t / (x * x)) - (c * n / (x * x))))),
                            int(round(x * ((c * t / (x * x)) - (c * t * n / (x ** 3))))),
                            int(round(x * ((t * n / (x * x)) - (c * t * n / (x ** 3))))),
                            int(round(x * ((c * n / (x * x)) - (c * t * n / (x ** 3))))),
                            int(round(x * ((c * t * n / (x ** 3))))), 0]

    #quando esta função for chamada pelo simulador, teremos o objeto global "listaquantidades".


#a próxima função é a conclusão de tudo. Ela recebe como parâmetros uma quantidade de dias mais os cortes, os tois e as negativações.
#Daí, depois, encontra totais desta nota para cada cidade com base nos rateios do dicionariorateio. Com estes valores, a função "dividindo"
#é chamada, retornando, a quantidade de notas em cada perfil. Os perfis são, então, multiplicados pelos alphas, somados e multiplicados
#pelo número de dias. Uma vez que os alphas significam a quantidade de processos que uma pessoa daquele perfil terá em um dia, temos uma simulação!
def simulacao(dias, cortes=None, tois=None, negativacoes=None):
    global dicionariorateio
    global dicionarioalphas
    global listaquantidades
    global resultado
    resultado = {}
    for chave in dicionariorateio:
        if cortes != None:
            c = cortes * dicionariorateio[chave][0]
        else:
            c = None
        if tois != None:
            t = tois * dicionariorateio[chave][1]
        else:
            t = None
        if negativacoes != None:
            n = negativacoes * dicionariorateio[chave][2]
        else:
            n = None
        dividindo(dicionariorateio[chave][3], c, t, n)
        processos = 0.0
        for x in range(9):
            processos += (float(dicionarioalphas[chave][x]) * listaquantidades[x])
        resultado[chave] = int(round(dias * processos))
    return resultado

# <codecell>

simulacao(9000)

# <codecell>


