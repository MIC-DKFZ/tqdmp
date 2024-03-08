from multiprocessing import Pool
from functools import partial
from tqdm import tqdm

_zip = zip


def ptqdm(function, iterable, processes, zip=False, unzip=False, chunksize=1, desc=None, disable=False, **kwargs):
    """
    Run a function in parallel with a tqdm progress bar and an arbitrary number of iterables and arguments.
    Multiple iterables can be packed into a tuple and passed to the 'iterable argument'. The iterables must be the first arguments in the function that is run in parallel.
    Results are always ordered and the performance is the same as of Pool.map.
    :param function: The function that should be parallelized.
    :param iterable: The iterable passed to the function.
    :param processes: The number of processes used for the parallelization. Use single-processing if number of processes is zero or None.
    :param zip: If multiple input iterables are passed as a single tuple to ptqdm. The iterables will be unpacked and passed as separate arguments to the function.
    :param unzip: If the function returns multiple outputs, the ptqdm result is a list of output tuples. If unzip is True, the list is unpacked such that ptqdm returns instead a tuple of output lists.
    :param chunksize: The iterable is based on the chunk size chopped into chunks and submitted to the process pool as separate tasks.
    :param desc: The description displayed by tqdm in the progress bar.
    :param disable: Disables the tqdm progress bar.
    :param kwargs: Any additional arguments that should be passed to the function.
    """
    if kwargs:
        function_wrapper = partial(wrapper, function=function, zip=zip, **kwargs)
    else:
        function_wrapper = partial(wrapper, function=function, zip=zip)

    if zip:
        length = len(iterable[0])
        iterable = _zip(*iterable)
    else:
        length = len(iterable)

    results = [None] * length

    if (processes is None) or (processes == 0):
        for i, value in enumerate(tqdm(iterable, desc=desc, total=length, disable=disable)):
            results[i] = function_wrapper((i, value))[1]
    else:
        with Pool(processes=processes) as p:
            with tqdm(desc=desc, total=length, disable=disable) as pbar:
                for i, result in p.imap_unordered(function_wrapper, enumerate(iterable), chunksize=chunksize):
                    results[i] = result
                    pbar.update()

    if unzip:
        unzipped_results = [[] for i in range(len(results[0]))]
        for i in range(len(results)):
            for j in range(len(unzipped_results)):
                unzipped_results[j].append(results[i][j])
        results = unzipped_results

    return results


def wrapper(enum_iterable, function, zip, **kwargs):
    i = enum_iterable[0]
    if zip:
        result = function(*enum_iterable[1], **kwargs)
    else:
        result = function(enum_iterable[1], **kwargs)
    return i, result