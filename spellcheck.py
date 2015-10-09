import numpy as np
import sys


def get_args():
    to_check = str(sys.argv[1])
    dictionary = str(sys.argv[2])

    return to_check, dictionary


def parse_txt(input_file_name):
    doc = open(input_file_name)
    text = doc.read()
    words = text.split()
    return words


def levenshtein_distance(word1, word2, del_cost, ins_cost, sub_cost):
    m = len(word1)
    n = len(word2)
    d = np.zeros((m+1, n+1))

    for i in range(m+1):
        d[i, 0] = i*del_cost
    for j in range(n+1):
        d[0, j] = j*ins_cost

    for j in range(1, n+1):
        for i in range(1, m+1):
            if word1[i-1] == word2[j-1]:
                d[i, j] = d[i-1, j-1]
            else:
                d[i, j] = min(d[i-1, j] + del_cost,
                              d[i, j-1] + ins_cost,
                              d[i-1, j-1] + sub_cost)

    return d[m, n]


def find_closest_word(string, dictionary, del_cost, ins_cost, sub_cost):
    distances = [1000] * len(dictionary)
    for i in range(len(dictionary)):
        distances[i] = levenshtein_distance(string, dictionary[i], del_cost, ins_cost, sub_cost)
    val, idx = min((val, idx) for (idx, val) in enumerate(distances))
    return dictionary[idx]


def spellcheck():

    to_check, dictionary = get_args()
    to_check = parse_txt(to_check)
    dictionary = parse_txt(dictionary)

    correct_words = [0] * len(to_check)
    for j, word in enumerate(to_check):
        correction = find_closest_word(word, dictionary)
        correct_words[j] = correction

    f = open('corrected.txt', 'w')
    for word in correct_words:
        f.write("%s " % word)
    f.close()
