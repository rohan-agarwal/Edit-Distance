# ------------------------------
# Recreation of the pipelines from spellcheck, measure_error, and hour_test
# Using a qwerty-Levenshtein distance, which specifies substitution costs
# Costs are determined based on distance between letters on a keyboard
# This is implemented using a coordinate system with the 'q' key being the origin
# ------------------------------

from measure_error import *
from matplotlib import pyplot as plt


# Compute the manhattan distance (L1 norm) between two points
def manhattan_dist(a, b):
    dist = 0
    for i in range(len(a)):
        dist = dist + abs(b[i]-a[i])

    return dist

# qwerty-edited functions from spellcheck/measure_error/hour_test

def qwerty_levenshtein_distance(word1, word2, del_cost, ins_cost):
    word1 = filter(lambda x: x not in '!@#$%^&*()_+-=:;<>,./?\'\"', word1)
    word1 = word1.lower()
    word2 = filter(lambda x: x not in '!@#$%^&*()_+-=:;<>,./?\'\"', word2)
    word2 = word2.lower()

    m = len(word1)
    n = len(word2)
    d = np.zeros((m+1, n+1))

    positions = {'q': (0, 0), 'w': (1, 0), 'e': (2, 0), 'r': (3, 0),
                 't': (4, 0), 'y': (5, 0), 'u': (6, 0), 'i': (7, 0),
                 'o': (8, 0), 'p': (9, 0), 'a': (0, 1), 's': (1, 1),
                 'd': (2, 1), 'f': (3, 1), 'g': (4, 1), 'h': (5, 1),
                 'j': (6, 1), 'k': (7, 1), 'l': (8, 1), 'z': (0, 2),
                 'x': (1, 2), 'c': (2, 2), 'v': (3, 2), 'b': (4, 2),
                 'n': (5, 2), 'm': (6, 2), '1': (0, -1), '2': (1, -1),
                 '3': (2, -1), '4': (3, -1), '5': (4, -1), '6': (5, -1),
                 '7': (6, -1), '8': (7, -1), '9': (8, -1), '0': (9, -1)}

    for i in range(m+1):
        d[i, 0] = i*del_cost
    for j in range(n+1):
        d[0, j] = j*ins_cost

    for j in range(1, n+1):
        for i in range(1, m+1):
            if word1[i-1] == word2[j-1]:
                d[i, j] = d[i-1, j-1]
            else:
                sub_cost = manhattan_dist(positions[word1[i-1]],
                                          positions[word2[j-1]])
                d[i, j] = min(d[i-1, j] + del_cost,
                              d[i, j-1] + ins_cost,
                              d[i-1, j-1] + sub_cost)

    return d[m, n]


def closest_qwerty(string, dictionary, del_cost, ins_cost):
    distances = [1000] * len(dictionary)
    for i in range(len(dictionary)):
        distances[i] = qwerty_levenshtein_distance(string, dictionary[i], del_cost, ins_cost)
    val, idx = min((val, idx) for (idx, val) in enumerate(distances))
    return dictionary[idx]


def qwerty_measure_error(typos, truewords, dictionarywords, del_cost, ins_cost):
    matches = [0] * len(typos)
    for i, word in enumerate(typos):
        correction = closest_qwerty(word, dictionarywords, del_cost, ins_cost)
        if correction != truewords[i]:
            matches[i] = 1

    error_rate = float(sum(matches))/float(len(matches))
    return error_rate


def qwerty_test(parameter_range, num_typos, dict_length):
    typos, truewords, dictionarywords = get_default_data()
    parameter_values = []
    errors = []
    start = time.time()
    for i in parameter_range:
        for j in parameter_range:
                parameter_values.append([i, j])
                errors.append(qwerty_measure_error(typos[0:num_typos],
                                                   truewords[0:num_typos],
                                                   dictionarywords[0:dict_length],
                                                   i, j))
    stop = time.time()

    total_time = stop - start
    val, idx = min((val, idx) for (idx, val) in enumerate(errors))
    best_parameters = parameter_values[idx]

    return total_time, best_parameters, parameter_values, errors


def qwerty_plots(param_values, errors):
    del_cost = [x[0] for x in param_values]
    ins_cost = [x[1] for x in param_values]

    plt.subplot(121)
    plt.scatter(del_cost, errors)
    plt.title('del_cost')
    plt.subplot(122)
    plt.scatter(ins_cost, errors)
    plt.title('ins_cost')

total_time2, best2, param_values2, errors2 = qwerty_test([0, 1, 2, 4, 8], 211, 4503)
qwerty_plots(param_values2, errors2)
