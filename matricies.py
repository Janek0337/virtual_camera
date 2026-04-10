import numpy as np
from math import sin, cos, tan
from main import Camera

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

def points_on_plain(points: np.ndarray, camera: Camera, width: int, height: int):
    scaling_coef = 1 / tan(camera.fov / 2)
    display_proportion = width / height
    projection_matrix = np.array([[scaling_coef/display_proportion, 0, 0, 0],
                                 [0, scaling_coef, 0, 0],
                                 [0, 0, 0, 1],
                                 [0, 0, 0, 0]])
    projected_points = points @ projection_matrix
    w = projected_points[:, 3].reshape(-1,1)
    w[w == 0] = 0.0001
    normalized_xy = projected_points[:, :2] / w
    
    normalized_x = normalized_xy[:, 0]
    normalized_y = normalized_xy[:, 1]

    scaled_x = (normalized_x + 1) * 0.5 * width
    scaled_y = (1 - normalized_y) * 0.5 * height

    return np.column_stack((scaled_x, scaled_y))

def transform_to_camera(punkty: np.ndarray, pozycja_kamery: tuple[float, float, float], katy: tuple[float, float]):
    cx, cy, cz = pozycja_kamery
    kat_poziom, kat_pion = katy
    stranslatowane = translacja(punkty, -cx, -cy, -cz)

    punkty_o_Y = obrot_wokol_Y(stranslatowane, -kat_poziom)
    punkty_o_X = obrot_wokol_X(punkty_o_Y, -kat_pion)

    return punkty_o_X