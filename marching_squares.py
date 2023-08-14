import numpy as np
from opensimplex import OpenSimplex
import pygame


class Marching_Square:
    display = None
    square_size = 0
    point_pos = [[0, 0], [square_size, 0], [square_size, square_size], [0, square_size]]
    point_dir = [[square_size, 0], [0, square_size], [-square_size, 0], [0, -square_size]]

    def __init__(self, pos):
        self.tl_point = 0.0
        self.tr_point = 0.0
        self.bl_point = 0.0
        self.br_point = 0.0
        self.mid_point = 0.0
        self.position = pos
        self.offset = [pos[0] * self.square_size, pos[1] * self.square_size]

    def update(self, tl, tr, mid, bl, br):
        self.tl_point = tl
        self.tr_point = tr
        self.bl_point = bl
        self.br_point = br
        self.mid_point = mid

    def print_values(self):
        print(f"{self.tl_point}    {self.tr_point}")
        print(f"{self.bl_point}    {self.br_point}")

    def draw_lines(self, color=(0, 0, 0)):
        line_thickness = 4
        square = [self.tl_point, self.tr_point, self.br_point, self.bl_point]

        points = []
        for i, a in enumerate(square):
            b = square[(i + 1) % 4]
            if a * b < 0:
                interpolation_point = -a / (b - a)
                point = [self.point_pos[i][0] + interpolation_point * self.point_dir[i][0],
                         self.point_pos[i][1] + interpolation_point * self.point_dir[i][1]]
                points.append(point)

        lines = []
        if len(points) == 2:
            lines.append([points[0], points[1]])
        elif len(points) == 4:
            if self.mid_point * self.tl_point >= 0:
                lines.append([points[0], points[3]])
                lines.append([points[1], points[2]])
            else:
                lines.append([points[0], points[3]])
                lines.append([points[1], points[2]])

        for line in lines:
            start_pos = [line[0][0] + self.position[0] * self.square_size,
                         line[0][1] + self.position[1] * self.square_size]
            end_pos = [line[1][0] + self.position[0] * self.square_size,
                       line[1][1] + self.position[1] * self.square_size]
            pygame.draw.line(self.display, color, start_pos, end_pos, line_thickness)

    @classmethod
    def set_class_vars(cls):
        cls.point_pos = [[0, 0], [cls.square_size, 0], [cls.square_size, cls.square_size], [0, cls.square_size]]
        cls.point_dir = [[cls.square_size, 0], [0, cls.square_size], [-cls.square_size, 0], [0, -cls.square_size]]


if __name__ == "__main__":
    rng = np.random.default_rng(seed=0)
    ix, iy, iz = rng.random(2), rng.random(1), rng.random(1)
    print(ix, iy, iz)
    noise = OpenSimplex(0)
    noise_val = OpenSimplex.noise3array(noise, ix, iy, iz)
    print(type(noise_val))
