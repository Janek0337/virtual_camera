import numpy as np
import cv2 as cv
import keyboard
import matricies

class Camera:
    def __init__(self, camera_data):
        self.cx = camera_data[0]
        self.cy = camera_data[1]
        self.cz = camera_data[2]
        self.kat_poziom = camera_data[3]
        self.kat_pion = camera_data[4]
        self.speed = 5
        self.fov = 90
        self.kat_speed = 15

    def get_position(self):
        return (self.cx, self.cy, self.cz)
    
    def get_angle(self):
        return (self.kat_poziom, self.kat_pion)
    
    def handle_input(self, event):
        if event.event_type == 'down':
            if event.name == 'w':
                self.cz += self.speed
            elif event.name == 's':
                self.cz -= self.speed
            elif event.name == 'a':
                self.cx -= self.speed
            elif event.name == 'd':
                self.cx += self.speed
            elif event.name == 'q':
                self.cy -= self.speed
            elif event.name == 'e':
                self.cy += self.speed
            elif event.name == 'up':
                self.kat_pion += self.kat_speed
            elif event.name == 'down':
                self.kat_pion -= self.kat_speed
            elif event.name == 'right':
                self.kat_poziom += self.kat_speed
            elif event.name == 'left':
                self.kat_poziom -= self.kat_speed

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
    return (Camera(camera_pos), all_points)

def make_point_matrix(all_points: list[tuple[list[float], list[float]]]):
    matrix = np.array(all_points)
    points3d = matrix.reshape(-1, 3)

    ones = np.ones((points3d.shape[0], 1))
    points4d = np.hstack((points3d, ones))

    return points4d

def main():
    camera, all_pts = read_input()
    
    print(make_point_matrix(all_pts))
    width = 1000
    height = 600

    keyboard.hook(camera.handle_input)
    while True:
        if keyboard.is_pressed('esc'):
            break
        if keyboard.is_pressed('alt'):
            print(f'Pozycja kamery: {camera.get_position()}; {camera.get_angle()}')

def transformacja_wzgledem_kamery(punkty: np.ndarray, pozycja_kamery: tuple[float, float, float], kat_poziom: float, kat_pion: float):
    cx, cy, cz = pozycja_kamery
    stranslatowane = matricies.translacja(punkty, -cx, -cy, -cz)
    
    kat_poziom_rad = np.radians(-kat_poziom)
    kat_pion_rad = np.radians(-kat_pion)

    punkty_o_Y = matricies.obrot_wokol_Y(stranslatowane, kat_poziom_rad)
    punkty_o_X = matricies.obrot_wokol_X(punkty_o_Y, kat_pion_rad)

    return punkty_o_X

"""
color = (255,255,255)
    img = np.full((width ,height, 3), 255, dtype=np.uint8)
    cv.line(img, (256, -50), (-50, 256), color=color, thickness=2)
    cv.imshow("Usmiechnij sie, jestes w ukrytej kamerze", img)
    keyboard.hook(on_key_event)
    while True:
        i += 1
        i %= 256
        color = (i % 256,(i - 67) % 256,(2*i) % 256)
        cv.line(img, (256, -50), (-50, 256), color=color, thickness=2)
        cv.imshow("Usmiechnij sie, jestes w ukrytej kamerze", img)
        if cv.waitKey(1) & 0xFF == 27:
            break
        if keyboard.is_pressed('esc'):
            break
    cv.destroyAllWindows()
"""
if __name__ == "__main__":
    main()
