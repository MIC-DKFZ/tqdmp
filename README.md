# tqdmp

[![License MIT](https://img.shields.io/pypi/l/tqdmp.svg?color=green)](https://github.com/Karol-G/tqdmp/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/tqdmp.svg?color=green)](https://pypi.org/project/tqdmp)
[![Python Version](https://img.shields.io/pypi/pyversions/tqdmp.svg?color=green)](https://python.org)
[![tests](https://github.com/Karol-G/tqdmp/workflows/tests/badge.svg)](https://github.com/Karol-G/tqdmp/actions)
[![codecov](https://codecov.io/gh/Karol-G/tqdmp/branch/main/graph/badge.svg)](https://codecov.io/gh/Karol-G/tqdmp)

Multiprocessing with tqdm progressbars!

Did you feel like you are missing a progressbar when using doing multiprocessing with `pool.map`? Well no more! `tqdmp` is an easy to use wrapper for `pool.map` but with a tqdm progressbar. Moreover it supports some nice usecases making multiprocessing much simpler:

- Use multiple iterables by simply packing them as a tuple
- Unpack the function output of the parallized function in case it returns multiple variables
- Switch to single processing by setting the number of processes to `None` or `0`
- Pass additional constant varibales to the parallized function as kwargs 

Examples of these usecases are given in section `Examples`.

## Installation

You can install `tqdmp` via [pip](https://pypi.org/project/tqdmp/):

    pip install tqdmp

## Examples

In the following we demonstrate the general useage of tqdmp and some useful features.

### Default multiprocessing
Using `pool.map`:
```python
from multiprocessing import Pool

def function(index):
    return index * 10

pool = Pool(2)
result = pool.map(function, range(10))
print(f"pool.map: {result}")
```

Using `tqdmp`:
```python
from tqdmp import tqdmp

def function(index):
    return index * 10

result = tqdmp(function, range(10), 2)
print(f"tqdmp: {result}")
```

### Multiple iterables
Using `pool.map`:
```python
from multiprocessing import Pool

def function(input_tuple):
    index1, index2 = input_tuple
    return index1 * index2

pool = Pool(2)
result = pool.map(function, zip(range(10), range(10)))
print(f"pool.map: {result}")
```

Using `tqdmp`:
```python
from tqdmp import tqdmp

def function(index1, index2):
    return index1 * index2

result = tqdmp(function, (range(10), range(10)), 2, mult_iter=True)
print(f"tqdmp: {result}")
```

### Multiple outputs
Using `pool.map`:
```python
from multiprocessing import Pool

def function(index1):
    return index1, index1 * 10

pool = Pool(2)
result = pool.map(function, range(10))
result1, result2  = map(list, zip(*result))
print(f"pool.map result1: {result1}")
print(f"pool.map result2: {result2}")
```

Using `tqdmp`:
```python
from tqdmp import tqdmp

def function(index1):
    return index1, index1 * 10

result1, result2 = tqdmp(function, range(10), 2, mult_out=True)
print(f"tqdmp result1: {result1}")
print(f"tqdmp result2: {result2}")
```

### Switching between single- and multiprocessing
Using `pool.map`:
```python
from multiprocessing import Pool

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
```

Using `tqdmp`:
```python
from tqdmp import tqdmp

def function(index):
    return index * 10

result = tqdmp(function, range(10), None)  # None or 0 for single, >0 for multi
print(f"tqdmp: {result}")
```

### Passing additional constant variables
Using `pool.map`:
```python
from multiprocessing import Pool
from functools import partial

def function(index, const1, const2):
    return (index * const1) + const2

pool = Pool(2)
partial_func = partial(function, const1=5, const2=7)
result = pool.map(partial_func, range(10))
print(f"pool.map: {result}")
```

Using `tqdmp`:
```python
from tqdmp import tqdmp

def function(index, const1, const2):
    return (index * const1) + const2

result = tqdmp(function, range(10), 2, const1=5, const2=7)
print(f"tqdmp: {result}")
```

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"tqdmp" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt

[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
