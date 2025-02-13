import random

import numpy as np
import pytest

import src.utils as utils


class TestUtils:

    @classmethod
    def setup_class(cls):
        cls.seed = 91

    def test_fix_seed_with_self_args(self):
        """Normal test;
        Run fix_seed and generate random integers through each module and do the same thing.

        Check if the generated integers are the same.
        """
        low = 0
        high = 100000

        utils.fix_seed(self.seed)
        x_random = random.randint(low, high)
        x_np = np.random.randint(low, high)

        utils.fix_seed(self.seed)
        assert x_random == random.randint(low, high)
        assert x_np == np.random.randint(low, high)
