# ------------------------------
# This file is dedicated for use with the wikipediatypo files and the 3esl dataset
# Here we assume that for the typos we know what the word was actually meant to be
# Based on this, can we get a measure of how good the algorithm finds the correction
# ------------------------------

import time
import csv
from spellcheck import *


# Function to parse data specifically in the format of wikipediatypo(clean).txt
def parse_data(input_file_name):
    data = []
    with open(input_file_name) as datafile:
        reader = csv.DictReader(datafile, delimiter="\t", fieldnames=['typo', 'correct'])
        for row in reader:
            data.append(row)

    return data


# Given that we know the "true" words for typos, what is our error in fixing typos?
def measure_error(typos, truewords, dictionarywords, del_cost, ins_cost, sub_cost):
    matches = [0] * len(typos)
    for i, word in enumerate(typos):
        correction = find_closest_word(word, dictionarywords, del_cost, ins_cost, sub_cost)
        if correction != truewords[i]:
            matches[i] = 1

    error_rate = float(sum(matches))/float(len(matches))
    return error_rate


# Function to get "default" data, that is data that the code was run on
def get_default_data():
    data = parse_data('wikipediatypoclean.txt')
    typos = [x['typo'] for x in data]
    truewords = [x['correct'] for x in data]
    dictionarywords = parse_txt('3esl.txt')
    return typos, truewords, dictionarywords


# Measuring the time for finding errors
# Parameters include number of typos, number of iterations, and dictionary size
def time_measure(n, rep, dict_length):
    typos, truewords, dictionarywords = get_default_data()
    times = []
    for i in range(rep):
        start = time.time()
        measure_error(typos[n*i:n*i+n], truewords[n*i:n*i+n], dictionarywords[0:dict_length], 1, 1, 1)
        stop = time.time()
        times.append(stop - start)
    mean_time = sum(times)/len(times)

    return mean_time
