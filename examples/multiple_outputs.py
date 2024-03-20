from multiprocessing import Pool
from tqdmp import tqdmp


def function(index1):
    return index1, index1 * 10


num_processes = 2
iterable = range(10)

pool = Pool(num_processes)
result = pool.map(function, iterable)
result1, result2  = map(list, zip(*result))
print(f"pool.map result1: {result1}")
print(f"pool.map result2: {result2}")

result1, result2 = tqdmp(function, iterable, num_processes, mult_out=True)
print(f"tqdmp result1: {result1}")
print(f"tqdmp result2: {result2}")