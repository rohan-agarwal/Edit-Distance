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


def plots(param_values, errors):
    del_cost = [x[0] for x in param_values]
    ins_cost = [x[1] for x in param_values]
    sub_cost = [x[2] for x in param_values]

    plt.subplot(131)
    plt.scatter(del_cost, errors)
    plt.title('del_cost')
    plt.subplot(132)
    plt.scatter(ins_cost, errors)
    plt.title('ins_cost')
    plt.subplot(133)
    plt.scatter(sub_cost, errors)
    plt.title('sub_cost')

total_time, best, param_values, errors = test([0, 1, 2], 211, 4503)
plots(param_values, errors)
