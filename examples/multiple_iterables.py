from multiprocessing import Pool
from tqdmp import tqdmp


def function1(input_tuple):
    index1, index2 = input_tuple
    return index1 * index2


def function2(index1, index2):
    return index1 * index2


num_processes = 2
iterable1 = range(10)
iterable2 = range(10)

pool = Pool(num_processes)
result = pool.map(function1, zip(iterable1, iterable2))
print(f"pool.map: {result}")

result = tqdmp(function2, (iterable1, iterable2), num_processes, mult_iter=True)
print(f"tqdmp: {result}")