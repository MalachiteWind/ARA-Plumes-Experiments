from typing import Literal
from typing import NewType

import numpy as np
from numpy.typing import NBitBase

NpFlt = np.dtype[np.floating[NBitBase]]

PolyData = np.ndarray[tuple[int, Literal[3]], NpFlt]
Float1D = np.ndarray[tuple[int], NpFlt]
Float2D = np.ndarray[tuple[int, int], NpFlt]

Frame = NewType("Frame", int)
PlumePoints = np.ndarray[tuple[int, Literal[3]], NpFlt]
