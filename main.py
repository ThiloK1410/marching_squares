import pygame
import numpy as np
from numpy import array
from opensimplex import OpenSimplex
from marching_squares import Marching_Square
from noise_handler import Noise_Handler

import cProfile
import pstats


class App:
    # main function from where everything is called
    def __init__(self):
        # initiating a clock and setting timer of the application
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.time_per_frame = 1000 / self.fps

        self._running = True
        self.display = None

        self.size = (800, 800)  # must be quadratic (for now)
        self.number_squares = 10
        self.square_size = self.size[0] / self.number_squares
        self.noise_dimension = self.number_squares * 2 + 1

        self.draw_raster = False

        self.marching_squares = [[] * self.number_squares for _ in range(self.number_squares)]

        self.noise_handler = Noise_Handler(array([self.noise_dimension, self.noise_dimension]), seed=1, details=5, threads=2)

        self.noise_vals = self.noise_handler.get_next_layer()

        self.current_z_layer = 0

    # called once to start program
    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        Marching_Square.display = self.display
        Marching_Square.square_size = self.square_size
        Marching_Square.set_class_vars()

        self.add_marching_squares()

        self.on_execute()

    # handles player inputs
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    # loop which will be executed at fixed rate (for physics, animations and such)
    def on_loop(self):
        self.noise_vals = self.noise_handler.get_next_layer()
        self.update_marching_squares()

    # loop which will only be called when enough cpu time is available
    def on_render(self):
        self.display.fill((255, 255, 255))

        self.draw_marching_squares()

        if self.draw_raster:
            self.draw_marching_squares_raster()

        pygame.display.update()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def on_execute(self):
        previous = pygame.time.get_ticks()
        lag = 0.0

        # advanced game loop to call on_loop() at fixed rate and on_render() as fast as possible
        # (kinda overkill right now) (also not relevant)
        while self._running:
            current = pygame.time.get_ticks()
            elapsed = current - previous
            lag += elapsed
            previous = current

            for event in pygame.event.get():
                self.on_event(event)

            while lag > self.time_per_frame:
                self.on_loop()
                lag -= self.time_per_frame
            self.on_render()
        self.on_cleanup()

    def add_marching_squares(self):
        for i in range(self.number_squares):
            for j in range(self.number_squares):
                self.marching_squares[i].append(Marching_Square([i, j]))

    def update_marching_squares(self):
        for i in range(self.number_squares):
            for j in range(self.number_squares):
                tl = self.noise_vals[i * 2][j * 2]
                tr = self.noise_vals[i * 2 + 2][j * 2]
                mid = self.noise_vals[i * 2 + 1][j * 2 + 1]
                bl = self.noise_vals[i * 2][j * 2 + 2]
                br = self.noise_vals[i * 2 + 2][j * 2 + 2]
                self.marching_squares[i][j].update(tl, tr, mid, bl, br)

    def draw_marching_squares(self):
        for i in range(self.number_squares):
            for j in range(self.number_squares):
                self.marching_squares[i][j].draw_lines()

    def draw_marching_squares_raster(self):
        for i in range(self.number_squares):
            pygame.draw.line(self.display, (0, 0, 0), [0, i * self.square_size], [self.size[0], i * self.square_size])
        for i in range(self.number_squares):
            pygame.draw.line(self.display, (0, 0, 0), [i * self.square_size, 0], [i * self.square_size, self.size[1]])


if __name__ == "__main__":
    app = App()
    app.on_init()

