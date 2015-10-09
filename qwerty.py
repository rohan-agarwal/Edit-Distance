from spellcheck import *


def manhattan_dist(a, b):
    dist = 0
    for i in range(len(a)):
        dist = dist + abs(b[i]-a[i])

    return dist


def qwerty_levenshtein_distance(word1, word2, del_cost, ins_cost):
    m = len(word1)
    n = len(word2)
    d = np.zeros((m+1, n+1))

    positions = {'q': (0, 0), 'w': (1, 0), 'e': (2, 0), 'r': (3, 0),
                 't': (4, 0), 'y': (5, 0), 'u': (6, 0), 'i': (7, 0),
                 'o': (8, 0), 'p': (9, 0), 'a': (0, 1), 's': (1, 1),
                 'd': (2, 1), 'f': (3, 1), 'g': (4, 1), 'h': (5, 1),
                 'j': (6, 1), 'k': (7, 1), 'l': (8, 1), 'z': (0, 2),
                 'x': (1, 2), 'c': (2, 2), 'v': (3, 2), 'b': (4, 2),
                 'n': (5, 2), 'm': (6, 2)}

    for i in range(m+1):
        d[i, 0] = i*del_cost
    for j in range(n+1):
        d[0, j] = j*ins_cost

    for j in range(1, n+1):
        for i in range(1, m+1):
            if word1[i-1] == word2[j-1]:
                d[i, j] = d[i-1, j-1]
            else:
                sub_cost = manhattan_dist(positions[word1[i]], positions[word2[j]])
                d[i, j] = min(d[i-1, j] + del_cost,
                              d[i, j-1] + ins_cost,
                              d[i-1, j-1] + sub_cost)

    return d[m, n]


def closest_qwerty(string, dictionary):
    distances = [1000] * len(dictionary)
    for i in range(len(dictionary)):
        distances[i] = qwerty_levenshtein_distance(string, dictionary[i], 1, 1, 1)
    val, idx = min((val, idx) for (idx, val) in enumerate(distances))
    return dictionary[idx]

