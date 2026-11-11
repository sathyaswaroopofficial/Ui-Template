import os
import random

import numpy as np


def set_seed(seed: int) -> None:
    """Make runs reproducible. Extend with torch.manual_seed(...) if you add PyTorch."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
