from numba import njit
import numpy as np
import glm
import math

WIN_RES = glm.vec2(1600, 900)
BG_COLOR = glm.vec3(0.2, 0.25, 0.42)