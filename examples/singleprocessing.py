from multiprocessing import Pool
from tqdmp import tqdmp


def function(index):
    return index * 10


num_processes = None  # None or 0 for single, >0 for multi
iterable = range(10)

if (num_processes is None) or (num_processes == 0):
    result = [function(index) for index in iterable]
else:
    pool = Pool(num_processes)
    result = pool.map(function, iterable)
print(f"pool.map: {result}")

result = tqdmp(function, range(10), None)
print(f"tqdmp: {result}")