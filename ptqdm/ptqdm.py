from multiprocessing import Pool
from functools import partial
from tqdm import tqdm
from typing import Callable, Iterable, List, Tuple, Any, Optional

_zip = zip


def ptqdm(
    function, #: Callable[..., Any],
    iterable, #: Iterable[Any] | Tuple[Iterable[Any], ...],
    processes: Optional[int],
    zip: bool = False,
    unzip: bool = False,
    chunksize: int = 1,
    desc: Optional[str] = None,
    disable: bool = False,
    **kwargs: Any
): # -> List[Any] | Tuple[List[Any], ...]:
    """
    Executes a function in parallel across multiple processes, optionally with progress tracking via tqdm.
    
    This function enhances the standard multiprocessing.Pool by integrating a tqdm progress bar, allowing for easy progress monitoring of parallel tasks. 
    It supports both single and multiple input iterables, as well as functions that return multiple outputs.

    Parameters:
    - function (callable): The function to be executed in parallel. It should accept the elements of `iterable` as its first arguments.
    - iterable (iterable): An iterable (or a tuple of iterables if `zip` is True) whose elements are passed as arguments to `function`.
    - processes (int): The number of worker processes to use. If 0 or None, runs synchronously in the main process.
    - zip (bool, optional): If True and `iterable` is a tuple of iterables, elements from each iterable are combined using `zip` and passed as separate arguments to `function`.
    - unzip (bool, optional): If True and `function` returns a tuple of values, the output is a tuple of lists, each containing elements from the corresponding position in the output tuples.
    - chunksize (int, optional): The number of tasks dispatched to each worker process at a time. This can be adjusted to optimize performance.
    - desc (str, optional): Description text to display above the progress bar.
    - disable (bool, optional): If True, the tqdm progress bar is not displayed.
    - kwargs: Additional keyword arguments to pass to `function`.

    Returns:
    - List of results from applying `function` to elements of `iterable`, or, if `unzip` is True, a tuple of lists containing unpacked results.

    Notes:
    - Results are always returned in the order corresponding to the input iterable, mirroring the behavior of `Pool.map`.
    - The performance is the same as that of `Pool.map`.
    - The `function` can optionally accept keyword arguments if `kwargs` is provided.
    """
    
    # Wrapper for handling additional arguments and zipping/unzipping logic
    if kwargs:
        function_wrapper = partial(wrapper, function=function, zip=zip, **kwargs)
    else:
        function_wrapper = partial(wrapper, function=function, zip=zip)

    # Prepare iterable based on zip flag and compute length
    if zip:
        length = len(iterable[0])
        iterable = _zip(*iterable)
    else:
        length = len(iterable)

    results = [None] * length

    # Synchronous execution if processes is 0 or None
    if (processes is None) or (processes == 0):
        for i, value in enumerate(tqdm(iterable, desc=desc, total=length, disable=disable)):
            results[i] = function_wrapper((i, value))[1]
    else:
        # Parallel execution with Pool
        with Pool(processes=processes) as p:
            with tqdm(desc=desc, total=length, disable=disable) as pbar:
                for i, result in p.imap_unordered(function_wrapper, enumerate(iterable), chunksize=chunksize):
                    results[i] = result
                    pbar.update()

    # Unzip results if requested
    if unzip:
        unzipped_results = [[] for i in range(len(results[0]))]
        for i in range(len(results)):
            for j in range(len(unzipped_results)):
                unzipped_results[j].append(results[i][j])
        results = unzipped_results

    return results


def wrapper(enum_iterable, function, zip, **kwargs):
    """
    Internal helper function for applying the target function with or without zipping input arguments.
    
    Parameters are similar to `ptqdm`, tailored for internal use with multiprocessing.Pool.
    """
    i, args = enum_iterable
    if zip:
        result = function(*args, **kwargs)
    else:
        result = function(args, **kwargs)
    return i, result
