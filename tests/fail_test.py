import tempfile
import os
import random
import string
import unittest
from util4tests import run_single_test

# make a siple test that fails
class  TestSimpleFail(unittest.TestCase):
    def test_simple_fail(self):
        self.assertTrue(False)

if __name__ == '__main__':
   run_single_test(__file__)