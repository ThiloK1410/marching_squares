Visualizing Noise from OpenSimplexNoise on a PyGame window with the marching squares algorithm.

External Modules:
    - Numpy
    - Pygame
    - OpenSimplex

Variables to change (in main):
    - FPS (also rate at which noise moves through z axis)
    - noise_details (similar to noise octaves, higher values -> more detail)
    - number_squares (amount of marching squares per axis -> total amount = number_squares^2)
    - noise_buffer_size (size of the z axis buffer, noise handler tries to keep it filled) (no meaningful impact)
    - noise_handler_threads (number of threads/processes which try to keep buffer filled)
    - draw_raster (if set to True, grid of the marching squares is drawn)
    - move_through_z (actually main feature of my program, but can be turned off to create a single image, e.g. when fps and number_squares are too high)
    - size (size of the main window, please keep quadratic, otherwise program wont work as intended)