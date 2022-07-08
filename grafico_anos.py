import matplotlib.pyplot as plt
from leituras import anos_melhores


def grafico_anos(dicio):
    names = list(dicio.keys())
    values = list(dicio.values())
    fig = plt.subplots(figsize=(9, 3))
    plt.plot(names, values, color='red')
    plt.suptitle('Quantidade de artistas com Score 10 ao longo dos anos')
    return plt.savefig('static/images/anos_melhores.png')


g_a = grafico_anos(anos_melhores)
