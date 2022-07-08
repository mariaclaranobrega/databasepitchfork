def dicionario(artistas, generos):
    dicio = {}
    # Percorrendo os artistas
    for ida, artista in artistas:
        # Em cada artista, percorre os géneros
        for idg, genero in generos:
            # Se o ID do artista é igual ao género
            if ida == idg:
                # Se esse ID já estiver presente no dicionário (género)
                if idg in dicio.keys():
                    dicio[ida]["Género"].append(genero)
                # Se esse ID não existir
                elif idg not in dicio.keys():
                    # Se o artista tiver na lista, mas o género não
                    if artista in dicio.values() and genero not in dicio[idg]['Género']:
                        dicio[idg]['Género'].append(genero)
                        break
                    # Se o artista não tiver na lista
                    elif list(dicio.values()).count(artista) == 0 and str(dicio.values()).find(artista) == -1:
                        dicio[ida] = {"Artista": artista, "Género": [genero, ]}
    return dicio


def genero_dict(dicio,genero):
    listaartistas = []
    for ids, valores in dicio.items():
        if genero in valores['Género']:
            listaartistas.append(str(valores['Artista']).title())
    return listaartistas

