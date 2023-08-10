from numba import njit
import numpy as np
import glm
import math
import pygame as pg
import os

WIN_RES = glm.vec2(640*2, 480*2)
DISPLAY = [320*2, 240*2]
BG_COLOR = glm.vec3(0.0, 0.0, 0.0)