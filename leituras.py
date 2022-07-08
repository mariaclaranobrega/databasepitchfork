import sqlite3
import pandas as pd
from termcolor import colored


def interagir(query, parametros=()):
    with sqlite3.connect("database/database.sqlite") as file:
        cursor = file.cursor()
        interacao = cursor.execute(query, parametros)
        return interacao


info_consulta_review = interagir(query="SELECT * FROM pragma_table_info('reviews')")
info_review = info_consulta_review.fetchall()

review_consulta = interagir("SELECT reviewid,artist,score,pub_year FROM reviews ORDER BY reviewid ASC")
review_data = review_consulta.fetchall()


def melhores_artistas(lista):
    ordenar = interagir(query="SELECT reviewid,artist,score,pub_year FROM reviews ORDER BY score DESC")
    lista_ordenada = ordenar.fetchall()
    selecao = []
    for x in lista_ordenada:
        if x[2] == 10:
            selecao.append(x)
    return selecao


artistas_melhores = melhores_artistas(review_data)


def melhores_anos(lista):
    dicio = {}
    for i in lista:
        if i[3] in dicio.keys():
            dicio[i[3]] += 1
        else:
            dicio[i[3]] = 1
    return dicio


anos_melhores = melhores_anos(artistas_melhores)
media = sum(anos_melhores.values()) / len(anos_melhores)
media_str = '{:.2}'.format(media)
lista_anos_acima_media = [x[0] for x in anos_melhores.items() if x[1] > media]
anos_acima_media = ''
contador = 0
for i in lista_anos_acima_media:
    if contador < len(lista_anos_acima_media) - 1:
        anos_acima_media += (str(i) + ", ")
    else:
        anos_acima_media += (str(i))
    contador += 1


def nome_artistas(artistas, anos):
    lista = []
    dicio = {}
    for k in artistas:
        if k[2] == 10 and k[3] in anos:
            lista.append([str(k[1]).title(), k[3]])
    for j in lista:
        if j[1] in dicio.keys():
            if j[0] not in dicio[j[1]]:
                dicio[j[1]].append(j[0])
        else:
            dicio[j[1]] = [j[0], ]
    return dicio


"""def index(dicio):
    tamanho = 0
    for val in dicio.values():
        if len(val) > tamanho:
            tamanho = len(val)
    return tamanho
"""

artistas_acima_media = nome_artistas(artistas_melhores, lista_anos_acima_media)
# ind = index(artistas_acima_media)

serie_artistas = pd.Series(artistas_acima_media.values(), index=[x for x in artistas_acima_media.keys()])

str_melhores_artistas = ''
c = 0
while c < len(serie_artistas.keys()):
    str_melhores_artistas += (str(serie_artistas.keys()[c]) + ' - ' +
                              str(serie_artistas.values[c]).replace("[", "").replace("]", "").replace("'", "") + '\n')
    c += 1


def reviravolta():
    lista = []
    for chave, valores in artistas_acima_media.items():
        for valor in valores:
            info = interagir(query="SELECT artist,score,pub_year FROM reviews WHERE artist=? AND score<=? AND "
                                   "artist!='various artists'",
                             parametros=(valor.lower(), media))
            data = info.fetchall()
            lista.append(data)
    listagem = [x for x in lista if len(x) > 0]
    return listagem


info_reviravolta = reviravolta()
artistas_reviravolta = []
for arts in info_reviravolta:
    for nome, scorebaixo, ano in arts:
        artistas_reviravolta += [[[f"Nome: {nome.title()}"], [f"Score: {scorebaixo}"], [f"Ano: {ano}"]],]

