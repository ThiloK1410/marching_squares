import numpy as np
from opensimplex import OpenSimplex
from numpy import array
import concurrent.futures
import multiprocessing


# handles the z layer of a 3d noise using threads and reassigning of existing array
class Noise_Handler:
    def __init__(self, xy_shape: array, seed: int, details: int, threads: int = None, buffer_size: int = 20):
        if threads is None:
            threads = multiprocessing.cpu_count()
        self.threads = threads
        self.seed = seed
        self.buffer_size = buffer_size   # amount of simultaneously stored noise layers
        self.current_layer = 0
        self.buffer_size_loaded = 0

        self.noise = OpenSimplex(seed)
        self.detail = details         # similar to noise octaves

        # scaling down xy_shape to [0, 1], scales up with self.detail
        self.xy_coordinates = array([range(xy_shape[0]), range(xy_shape[1])]) / (xy_shape.reshape((2, 1)) / self.detail)

        self.executor = concurrent.futures.ThreadPoolExecutor(threads)
        self.values = np.empty(shape=(self.buffer_size, xy_shape[0], xy_shape[1]))

    @staticmethod
    def _fill(index: int, noise, xy_coordinates):
        index = array([index])
        noise_vals = noise.noise3array(xy_coordinates[0], xy_coordinates[1], index/100)
        return noise_vals

    def fill(self):

        threads = []
        for i in range(min(self.threads, self.buffer_size - self.buffer_size_loaded)):
            index = self.current_layer + self.buffer_size_loaded + i
            threads.append(self.executor.submit(self._fill, index, self.noise, self.xy_coordinates))

        for future in threads:
            try:
                result = future.result()
                self.values[(self.current_layer + self.buffer_size_loaded) % self.buffer_size] = result
                self.buffer_size_loaded += 1
            except Exception as e:
                print(f"Exception: {e}")
        # print(f"after fill was called the buffer_size_loaded is {self.buffer_size_loaded} / {self.buffer_size}")

    def get_next_layer(self):
        if self.buffer_size_loaded < self.buffer_size / 2:
            self.fill()
        index = self.current_layer % self.buffer_size
        self.current_layer += 1
        if self.buffer_size_loaded == 0:
            raise ValueError("Buffer not loaded")
        else:
            self.buffer_size_loaded -= 1
            return self.values[index]

    def __del__(self):
        self.executor.shutdown(False)


if __name__ == "__main__":
    noise = Noise_Handler(array([201, 201]), seed=1, details=1)

    for i in range(50):
        out = noise.get_next_layer()
        print(out.shape)
