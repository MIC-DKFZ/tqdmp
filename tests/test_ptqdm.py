from ptqdm import ptqdm
import numbers
import unittest


class TestPtqdm(unittest.TestCase):
    def test_single_iterable_single_argument(self, iterations=30, processes=10):
        iterable = range(0, iterations)
        y_single = [method(index1) for index1 in iterable]
        y_multi = ptqdm(method, iterable, processes)
        self.assertEqual(y_single, y_multi)

    def test_single_iterable_multiple_arguments(self, iterations=30, processes=10, arg1=5):
        iterable = range(0, iterations)
        y_single = [method(index1, arg1=arg1) for index1 in iterable]
        y_multi = ptqdm(method, iterable, processes, arg1=arg1)
        self.assertEqual(y_single, y_multi)

    def test_multiple_iterables_single_argument(self, iterations=30, processes=10):
        iterable1 = range(0, iterations)
        iterable2 = range(5, iterations+5)
        y_single = [method(index1, index2) for index1, index2 in zip(iterable1, iterable2)]
        y_multi = ptqdm(method, (iterable1, iterable2), processes, mult_iter=True)
        self.assertEqual(y_single, y_multi)

    def test_multiple_iterables_multiple_arguments(self, iterations=30, processes=10, arg1=5, arg2=7):
        iterable1 = range(0, iterations)
        iterable2 = range(5, iterations+5)
        y_single = [method(index1, index2, arg1=arg1, arg2=arg2) for index1, index2 in zip(iterable1, iterable2)]
        y_multi = ptqdm(method, (iterable1, iterable2), processes, mult_iter=True, arg1=arg1, arg2=arg2)
        self.assertEqual(y_single, y_multi)

    def test_multiple_iterables_multiple_arguments_multiple_outputs(self, iterations=30, processes=10, arg1=5, arg2=7):
        iterable1 = range(0, iterations)
        iterable2 = range(5, iterations+5)
        y_single = [method(index1, index2, arg1=arg1, arg2=arg2, multi_output=True) for index1, index2 in zip(iterable1, iterable2)]
        y_single1, y_single2 = zip(*y_single)
        y_multi1, y_multi2 = ptqdm(method, (iterable1, iterable2), processes, mult_iter=True, mult_out=True, arg1=arg1, arg2=arg2, multi_output=True)
        self.assertEqual(list(y_single1), y_multi1)
        self.assertEqual(list(y_single2), y_multi2)


def method(index1, index2=1, arg1=None, arg2=None, multi_output=False):
    if isinstance(arg1, numbers.Number):
        index1 = index1 * arg1
    if isinstance(arg2, numbers.Number):
        index2 = index2 * arg2
    if not multi_output:
        return index1 * index2
    else:
        return index1, index2