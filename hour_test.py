from measure_error import *
from matplotlib import pyplot as plt


def test(parameter_range, num_typos, dict_length):
    typos, truewords, dictionarywords = get_default_data()
    parameter_values = []
    errors = []
    start = time.time()
    for i in parameter_range:
        for j in parameter_range:
            for k in parameter_range:
                parameter_values.append([i, j, k])
                errors.append(measure_error(typos[0:num_typos],
                                            truewords[0:num_typos],
                                            dictionarywords[0:dict_length],
                                            i, j, k))
    stop = time.time()

    total_time = stop - start
    val, idx = min((val, idx) for (idx, val) in enumerate(errors))
    best_parameters = parameter_values[idx]

    return total_time, best_parameters, parameter_values, errors

total_time, best, param_values, errors = test([0, 1, 2], 3, 4503)
