from multiprocessing import Pool
from tqdmp import tqdmp


def function(index):
    return index * 10


num_processes = 2
iterable = range(10)

pool = Pool(num_processes)
result = pool.map(function, iterable)
print(f"pool.map: {result}")

result = tqdmp(function, iterable, num_processes)
print(f"tqdmp: {result}")