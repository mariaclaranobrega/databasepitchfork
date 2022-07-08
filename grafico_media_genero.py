from main import df_generos, media_generos
import matplotlib.pyplot as plt


def grafico_generos(df):
    nome_das_suas_colunas = df[df.columns[0]]
    valor_das_suas_colunas = df[df.columns[1]]

    plt.subplots(figsize=(13, 7))

    plt.barh([x.title() for x in nome_das_suas_colunas], valor_das_suas_colunas,
             color=['darkcyan', 'cadetblue', 'mediumturquoise', 'turquoise', 'aquamarine', 'lightskyblue',
                    'powderblue', 'lightcyan'])

    for index, value in enumerate(valor_das_suas_colunas):
        plt.text(value, index,
                 str(value))

    plt.title(f"Registros por Géneros")
    return plt.savefig('static/images/generos_registos.png')


g_generos = grafico_generos(df_generos)
