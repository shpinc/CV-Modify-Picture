import sys
import numpy as np
from Parameters import *

def select_random_path(E):
    # pentru linia 0 alegem primul pixel in mod aleator
    line = 0
    col = np.random.randint(low=0, high=E.shape[1], size=1)[0]
    pathway = [(line, col)]
    for i in range(E.shape[0]):
        # alege urmatorul pixel pe baza vecinilor
        line = i
        # coloana depinde de coloana pixelului anterior
        if pathway[-1][1] == 0:  # pixelul este localizat la marginea din stanga
            opt = np.random.randint(low=0, high=2, size=1)[0]
        elif pathway[-1][1] == E.shape[1] - 1:  # pixelul este la marginea din dreapta
            opt = np.random.randint(low=-1, high=1, size=1)[0]
        else:
            opt = np.random.randint(low=-1, high=2, size=1)[0]
        col = pathway[-1][1] + opt
        pathway.append((line, col))

    return pathway


def select_greedy_path(E):
    # pentru linia 0 alegem primul pixel cel cu energia cea mai mica
    line = 0

    col = np.argmin(E[0])

    pathway = [(line, col)]
    for i in range(1, E.shape[0]):
        # alege urmatorul pixel pe baza vecinilor
        line = i
        # coloana depinde de coloana pixelului anterior
        if pathway[-1][1] == 0:  # pixelul este localizat la marginea din stanga
            y = [E[line][col], E[line][col + 1]]
            x = min(y)
            opt = 0
            if x == E[line][col]:
                opt = 0
            if x == E[line][col + 1]:
                opt = 1
        elif pathway[-1][1] == E.shape[1] - 1:  # pixelul este la marginea din dreapta
            y = [E[line][col], E[line][col - 1]]
            x = min(y)
            opt = 0
            if x == E[line][col]:
                opt = 0
            if x == E[line][col - 1]:
                opt = -1
        else:
            y = [E[line][col], E[line][col + 1], E[line][col - 1]]
            x = min(y)
            opt = 0
            if x == E[line][col]:
                opt = 0
            if x == E[line][col - 1]:
                opt = -1
            if x == E[line][col + 1]:
                opt = 1
        col = pathway[-1][1] + opt
        pathway.append((line, col))

    return pathway

'''
def select_dynamic_path(E):
    # pentru linia 0 alegem primul pixel cel cu energia cea mai mica
    # line = 0
    # valoare = min(E[0])
    # col = np.argmin(E[0])
    # col = np.amin(E[0])
    # pathway = [(line, col)]

    Ecopy = E.copy()
    #adunam valorile din matrice dinamic
    #incepem de pe a doua linie, Ecopy[i][j] ia cea mai mica valoare de deasupra lui
    for i in range(1, Ecopy.shape[0]):
        for j in range(Ecopy.shape[1]):
            line = i
            col = j
            if j == 0: #suntem in marginea din stanga
                y = [Ecopy[line - 1][col], Ecopy[line - 1][col + 1]]
                x = min(y)
                Ecopy[line][col] += x
            elif j == Ecopy.shape[1] - 1: #suntem in marginea din dreapta
                y = [Ecopy[line - 1][col], Ecopy[line - 1][col - 1]]
                x = min(y)
                Ecopy[line][col] += x

            else:
                y = [Ecopy[line - 1][col], Ecopy[line - 1][col - 1], Ecopy[line - 1][col + 1]]
                x = min(y)
                Ecopy[line][col] += x


    costMinim = min(Ecopy[Ecopy.shape[0] - 1, :]) #costul minim final
    print(col)
    print(line)
    print(costMinim)
    #pozitia sfarsitului drumului de cost minim
    col =  np.argmin(Ecopy[Ecopy.shape[0] - 1, :])
    line = Ecopy.shape[0] - 1
    print(col)
    print(line)
    print(E[line][col])
    print(Ecopy)
    pathway = [(line, col)]
    for i in range(Ecopy.shape[0] - 2, -1, -1): #scot drumul incepand cu ultima linie astfel:
        # coloana depinde de coloana pixelului anterior
        if pathway[0][1] == 0:  # pixelul este localizat la marginea din stanga

            if Ecopy[line][col] - Ecopy[line - 1][col] == E[line][col]:
                opt = 0
            if Ecopy[line][col] - Ecopy[line - 1][col + 1] == E[line][col]:
                opt = 1


        elif pathway[0][1] == Ecopy.shape[1] - 1:  # pixelul este la marginea din dreapta

            if Ecopy[line][col] - Ecopy[line - 1][col] == E[line][col]:
                opt = 0
            if Ecopy[line][col] - Ecopy[line - 1][col - 1] == E[line][col]:
                opt = -1
        else:

            if Ecopy[line][col] - Ecopy[line - 1][col] == E[line][col]:
                opt = 0
            if Ecopy[line][col] - Ecopy[line - 1][col + 1] == E[line][col]:
                opt = 1
            if Ecopy[line][col] - Ecopy[line - 1][col - 1] == E[line][col]:
                opt = -1
        line = i
        col = pathway[-1][1] + opt
        pathway.insert(0, (line, col))



    #print(pathway)
    return pathway
'''
def select_dynamic_path(E):
    Suma = E.copy()
    n = Suma.shape[0]
    k = Suma.shape[1]

    for i in range(1, n):
        for j in range(0, k):
            mn_val = Suma[i - 1][j]
            if (j > 0):
                mn_val = min(mn_val, Suma[i - 1][j - 1])
            if (j + 1 < k):
                mn_val = min(mn_val, Suma[i - 1][j + 1])

            Suma[i][j] = E[i][j] + mn_val

    path = []
    y = 0
    for j in range(0, k):
        if (Suma[n - 1][j] < Suma[n - 1][y]):
            y = j

    path.append((n - 1, y))

    for x in range(n - 1, 0, -1):
        mn_val = Suma[x - 1][y]
        direction = 0

        if (y > 0 and Suma[x - 1][y - 1] < mn_val):
            mn_val = Suma[x - 1][y - 1]
            direction = -1
        if (y + 1 < k and Suma[x - 1][y + 1] < mn_val):
            mn_val = Suma[x - 1][y + 1]
            direction = +1

        y += direction
        path.insert(0, (x - 1, y))



    return (path)




def select_path(E, method):
    if method == 'aleator':
        return select_random_path(E)
    elif method == 'greedy':
        return select_greedy_path(E)
    elif method == 'programareDinamica':
        return select_dynamic_path(E)
    else:
        print('The selected method %s is invalid.' % method)
        sys.exit(-1)