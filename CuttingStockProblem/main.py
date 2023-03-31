from math import floor
from copy import deepcopy

L = 6
l_arr = [4, 3, 2]
d_arr = [50, 30, 35]
N = 3


def generate_efficient_patterns():
    result = []

    A_arr = [min(floor(L / l_arr[0]), d_arr[0])]
    for n in range(1, N):
        s = sum([A_arr[j] * l_arr[j] for j in range(n)])
        A_arr.append(min(floor((L - s) / l_arr[n]), d_arr[n]))

    while True:
        result.append(A_arr)

        for j in range(N - 2, -1, -1):
            if A_arr[j] > 0:
                k = j
                break
        else:
            return result

        A_arr_new = []
        for j in range(k):
            A_arr_new.append(A_arr[j])
        A_arr_new.append(A_arr[k] - 1)
        for n in range(k + 1, N):
            s = sum([A_arr_new[j] * l_arr[j] for j in range(n)])
            A_arr_new.append(min(floor((L - s) / l_arr[n]), d_arr[n]))
        A_arr = deepcopy(A_arr_new)


print(generate_efficient_patterns())
