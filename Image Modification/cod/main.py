A = [[10, 16, 9, 17, 18],
     [14, 18, 4, 15, 9],
     [16, 1, 8, 11, 2],
     [0, 3, 7, 4, 8],
     [16, 11, 13, 8, 1]]
def functie(A):
    Suma = A
    n = len(A)

    for i in range(1, n):
        for j in range(0, n):
            mn_val = Suma[i - 1][j]
            if (j > 0):
                mn_val = min(mn_val, Suma[i - 1][j - 1])
            if (j + 1 < n):
                mn_val = min(mn_val, Suma[i - 1][j + 1])

            Suma[i][j] = A[i][j] + mn_val

    road = []
    y = 0

    for j in range(0, n):
        if (Suma[n - 1][j] < Suma[n - 1][y]):
            y = j

    road.append((n - 1, y))

    for x in range(n - 1, 0, -1):
        mn_val = Suma[x - 1][y]
        direction = 0

        if (y > 0 and Suma[x - 1][y - 1] < mn_val):
            mn_val = Suma[x - 1][y - 1]
            direction = -1
        if (y + 1 < n and Suma[x - 1][y + 1] < mn_val):
            mn_val = Suma[x - 1][y + 1]
            direction = +1

        y += direction
        road.append((x - 1, y))

    road.reverse
    return (road)

print(functie(A))