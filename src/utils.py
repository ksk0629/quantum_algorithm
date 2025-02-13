import random

import numpy as np


def fix_seed(seed: int = 901):
    """Fix the random seeds to have reproducibility.

    :param int seed: random seed
    """
    random.seed(seed)

    np.random.seed(seed)
