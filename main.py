import numpy as np
import cv2 as cv
import keyboard
import matricies
from math import sin, cos

class Camera:
    def __init__(self, camera_data):
        self.cx = camera_data[0]
        self.cy = camera_data[1]
        self.cz = camera_data[2]
        self.kat_poziom = np.radians(camera_data[3])
        self.kat_pion = np.radians(camera_data[4])
        self.speed = 0.3
        self.fov = np.radians(camera_data[5])
        self.kat_speed = np.radians(10)
        self.fov_speed = np.radians(5)

    def get_position(self):
        return (self.cx, self.cy, self.cz)
    
    def get_angle(self):
        return (self.kat_poziom, self.kat_pion)
    
    def handle_input(self, event):
        if event.event_type == 'down':
            fx = sin(self.kat_poziom)
            fz = cos(self.kat_poziom)

            rx = cos(self.kat_poziom)
            rz = -sin(self.kat_poziom)

            if event.name == 'w':
                self.cz += fz * self.speed
                self.cx += fx * self.speed
            elif event.name == 's':
                self.cz -= fz * self.speed
                self.cx -= fx * self.speed
            elif event.name == 'a':
                self.cx -= rx * self.speed
                self.cz -= rz * self.speed
            elif event.name == 'd':
                self.cx += rx * self.speed
                self.cz += rz * self.speed
            elif event.name == 'q':
                self.cy -= self.speed
            elif event.name == 'e':
                self.cy += self.speed
            elif event.name == 'up':
                self.kat_pion -= self.kat_speed
            elif event.name == 'down':
                self.kat_pion += self.kat_speed
            elif event.name == 'right':
                self.kat_poziom += self.kat_speed
            elif event.name == 'left':
                self.kat_poziom -= self.kat_speed
            elif event.name == 'z':
                self.fov = max(np.radians(5), self.fov - self.fov_speed)
                print(f"FOV: {np.rad2deg(self.fov)}")
            elif event.name == 'x':
                self.fov = min(np.radians(120), self.fov + self.fov_speed)
                print(f"FOV: {np.rad2deg(self.fov)}")

def read_input():
    all_points = []
    with open('data.txt', 'r') as f:
        line = f.readline()
        camera_pos = line.strip().split(' ')
        if len(camera_pos) != 6:
            print('Zła liczba argumentów położenia kamery. Oczekiwane: (x, y, z, kat_poz, kat_pion, fov). Kąty w stopniach.')
            exit(1)
        camera_pos = [float(x) for x in camera_pos]
        camera_pos[3] = camera_pos[3] % 360
        camera_pos[4] = camera_pos[4] % 360
        camera = Camera(camera_pos)

        line = f.readline()
        while line:
            pts = line.strip().split(';')
            p1 = pts[0].strip().split(' ')
            p2 = pts[1].strip().split(' ')
            if len(p1) != 3 or len(p2) != 3:
                print(f'Linia: \"{line.strip()}\" zawiera niepoprawne punkty. Oczekiwany format: (x1 y1 z1; x1 y1 z1). Nie wczytuję tych punktów.')
                line = f.readline()
                continue
            p1 = [float(x) for x in p1]
            p2 = [float(x) for x in p2]
            all_points.append((p1, p2))
            line = f.readline()
    return (camera, all_points)

def make_point_matrix(all_points: list[tuple[list[float], list[float]]]):
    matrix = np.array(all_points)
    points3d = matrix.reshape(-1, 3)

    ones = np.ones((points3d.shape[0], 1))
    points4d = np.hstack((points3d, ones))

    return points4d

def main():
    width = 1000
    height = 600
    img = np.full((height, width, 3), 255, dtype=np.uint8)
    color = (0,0,0)

    camera, all_pts = read_input()
    base_pts = make_point_matrix(all_pts)

    all_pts = matricies.transform_to_camera(base_pts, camera.get_position(), camera.get_angle())
    points_on_plain = matricies.points_on_plain(all_pts, camera, width, height)

    keyboard.hook(camera.handle_input)
    while True:
        if keyboard.is_pressed('esc'):
            break
        if keyboard.is_pressed('alt'):
            print(f'Pozycja kamery: {camera.get_position()}; {camera.get_angle()}')

        transformed_pts = matricies.transform_to_camera(base_pts, camera.get_position(), camera.get_angle())
        points_on_plain = matricies.points_on_plain(transformed_pts, camera, width, height)

        img = np.full((height, width, 3), 255, dtype=np.uint8)
        for i in range(0, len(points_on_plain), 2):
            x1, y1 = points_on_plain[i, :]
            x2, y2 = points_on_plain[i+1, :]
            cv.line(img, (int(round(x1)), int(round(y1))), (int(round(x2)), int(round(y2))), color=color, thickness=2)
        cv.imshow("Usmiechnij sie, jestes w ukrytej kamerze", img)
        if cv.waitKey(16) & 0xFF == 27:
            break

    cv.destroyAllWindows()
    keyboard.unhook_all()

if __name__ == "__main__":
    main()
