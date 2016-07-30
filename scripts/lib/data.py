import numpy as np
import numpy.random as rand
import scipy.io as io

def batches(x0, y, n):
    order = rand.permutation(len(x0))
    x0_shuf = np.take(x0, order, axis=0)
    y_shuf = np.take(y, order, axis=0)
    for i in range(0, len(x0) - n + 1, n):
        yield x0_shuf[i:i+n], y_shuf[i:i+n]

class Dataset:
    def __init__(self, path):
        archive = io.loadmat(path)
        self.x0_tr = archive['x0_tr']
        self.x0_ts = archive['x0_ts']
        self.y_tr = archive['y_tr']
        self.y_ts = archive['y_ts']

        ϵ = 1e-3
        self.x0_tr = (
            (self.x0_tr - np.mean(self.x0_tr, (1, 2, 3), keepdims=True))
            / (np.std(self.x0_tr, (1, 2, 3), keepdims=True) + ϵ))
        self.x0_ts = (
            (self.x0_ts - np.mean(self.x0_ts, (1, 2, 3), keepdims=True))
            / (np.std(self.x0_ts, (1, 2, 3), keepdims=True) + ϵ))

    @property
    def x0_shape(self):
        return self.x0_tr.shape[1:]

    @property
    def y_shape(self):
        return self.y_tr.shape[1:]

    def training_batches(self, n=512):
        yield from batches(self.x0_tr, self.y_tr, n)

    def test_batches(self, n=512):
        yield from batches(self.x0_ts, self.y_ts, n)