import numpy as np
from math import sin, cos

def translacja(matrix: np.ndarray, Tx: float, Ty: float, Tz: float) -> np.ndarray:
    translation_matrix = np.array([[1,0,0,0],
                               [0,1,0,0],
                               [0,0,1,0],
                               [Tx,Ty,Tz,1]])
    return matrix @ translation_matrix

def obrot_wokol_X(matrix: np.ndarray, phi: float) -> np.ndarray:
    rotation_matrix = np.array([[1,0,0,0],
                               [0,cos(phi),sin(phi),0],
                               [0,-sin(phi),cos(phi),0],
                               [0,0,0,1]])
    return matrix @ rotation_matrix

def obrot_wokol_Y(matrix: np.ndarray, phi: float) -> np.ndarray:
    rotation_matrix = np.array([[cos(phi),0,-sin(phi),0],
                               [0,1,0,0],
                               [sin(phi),0,cos(phi),0],
                               [0,0,0,1]])
    return matrix @ rotation_matrix