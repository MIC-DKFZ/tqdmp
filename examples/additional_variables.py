from multiprocessing import Pool
from functools import partial
from tqdmp import tqdmp


def function(index, const1, const2):
    return (index * const1) + const2


num_processes = 2
iterable = range(10)

pool = Pool(num_processes)
partial_func = partial(function, const1=5, const2=7)
result = pool.map(partial_func, iterable)
print(f"pool.map: {result}")

result = tqdmp(function, iterable, num_processes, const1=5, const2=7)
print(f"tqdmp: {result}")