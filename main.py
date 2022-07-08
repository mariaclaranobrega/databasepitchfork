import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from dicionario import dicionario, genero_dict
import pandas as pd
import operator
from grafico_media_genero import *


def interagir(query, parametros=()):
    with sqlite3.connect("database/database.sqlite") as file:
        cursor = file.cursor()
        interacao = cursor.execute(query, parametros)
        return interacao


# Ler nome das colunas da tabela de artistas
info_consulta_artistas = interagir(query="SELECT * FROM pragma_table_info('artists')")
info_artistas = info_consulta_artistas.fetchall()

# Ler dados da tabela de artistas
artistas_consulta = interagir("SELECT * FROM artists ORDER BY reviewid")
artistas_data = artistas_consulta.fetchall()

# Ler nome das colunas da tabela de género
info_consulta_genero = interagir(query="SELECT * FROM pragma_table_info('genres')")
info_genero = info_consulta_genero.fetchall()
# Ler dados da tabela de gênero
genero_consulta = interagir("SELECT * FROM genres ORDER BY reviewid")
genero_data = genero_consulta.fetchall()

# Ler nome das colunas da tabela de anos
info_consulta_anos = interagir(query="SELECT * FROM pragma_table_info('years')")
info_anos = info_consulta_anos.fetchall()
# Ler dados da tabela de anos
anos_consulta = interagir("SELECT * FROM years ORDER BY reviewid")
anos_data = anos_consulta.fetchall()


def listar_generos(lista):
    generos = []
    for i in lista:
        if i[1] not in generos:
            generos.append(i[1])
    return generos


# ['rock', 'electronic', 'jazz', 'metal', 'rap', 'experimental', None, 'pop/r&b', 'global', 'folk/country']
lista_generos = listar_generos(genero_data)


def genero_quantidades(lista):
    generos = {'Não definido': 0, }
    for i in lista:
        if i[1] is None:
            generos['Não definido'] += 1
        elif i[1] in generos:
            generos[i[1]] += 1
        else:
            generos[i[1]] = 1
    return generos


# {'Não definido': 2367, 'rock': 9436, 'electronic': 3874, 'jazz': 435, 'metal': 860, 'rap': 1559,
# 'experimental': 1815, 'pop/r&b': 1432, 'global': 217, 'folk/country': 685}
quantidades_genero = genero_quantidades(genero_data)
generos_sorted = sorted(quantidades_genero.items(), key=operator.itemgetter(1))

# DataFrame (estrutura tabelar)
df_generos = pd.DataFrame(generos_sorted, index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Média dos registros por géneros
media_generos = df_generos.mean(numeric_only=True)

# Géneros com número de registros acima da média
generos_acima_media = df_generos[df_generos[1] >= media_generos[1]]
# Géneros com número de registros abaixo da média
generos_abaixo_media = df_generos[df_generos[1] < media_generos[1]]


# Ler dados da tabela de anos por ordem crescente
anos_interacao = interagir("SELECT * FROM years ORDER BY year")
anos_ordenado = anos_interacao.fetchall()


def anos_quantidades(lista):
    anos = {}
    for i in lista:
        if i[1] not in anos:
            anos[i[1]] = 1
        else:
            anos[i[1]] += 1
    return anos


# {None: 405, 1959: 0, 1960: 2, 1962: 2, 1963: 2, 1964: 4, 1965: 6, 1966: 7, 1967: 6, 1968: 15, 1969: 13,
# 1970: 17, 1971: 26, 1972: 14, 1973: 12, 1974: 10, 1975: 12, 1976: 9, 1977: 24, 1978: 10, 1979: 24, 1980: 24,
# 1981: 24, 1982: 16, 1983: 15, 1984: 10, 1985: 18, 1986: 6, 1987: 11, 1988: 15, 1989: 13, 1990: 20, 1991: 17,
# 1992: 24, 1993: 18, 1994: 25, 1995: 18, 1996: 32, 1997: 23, 1998: 22, 1999: 115, 2000: 219, 2001: 578,
# 2002: 965, 2003: 1029, 2004: 1045, 2005: 1215, 2006: 1181, 2007: 1264, 2008: 1176, 2009: 1148, 2010: 1138,
# 2011: 1139, 2012: 1178, 2013: 1199, 2014: 1133, 2015: 1152, 2016: 1204, 2017: 0}
quantidades_anos = anos_quantidades(anos_ordenado)

# Gráfico- Quantidade por genero
y_generos = list(quantidades_genero.values())
x_generos = [x.title() for x in list(quantidades_genero.keys())]

colors = ("DodgerBlue", "GreenYellow", "PaleVioletRed",
          "DimGray", "BlueViolet", "Lavender", "black", "Crimson", "Gold", "Coral")


def func(pct, allvalues):
    absolute = int(pct / 100. * np.sum(allvalues))
    return "{:.1f}%".format(pct, absolute)


def grafico():
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(y_generos,
                                      autopct=lambda pct: func(pct, y_generos),
                                      labels=x_generos,
                                      colors=colors,
                                      startangle=-10,
                                      textprops=dict(color="black"),
                                      wedgeprops=dict(width=0.5))
    plt.setp(autotexts, size=10)
    ax.set_title("Registro de artistas por géneros musicais")
    return fig.savefig('static/images/grafico_generos.png')


g = grafico()

"""
Gráfico pizza
fig = plt.figure(figsize=(10, 7))
plt.pie(y_generos, labels=x_generos)
"""

""" 
Gráfico barras
plt.bar(x_generos,y_generos, color="red")
plt.xticks(x_generos)
plt.ylabel('Quantidades')
plt.xlabel('Géneros Musicais')
plt.title('Géneros Musicais x Quantidade de artistas')
"""

