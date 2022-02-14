import numpy as np

a = np.zeros((5,3))
a[[1,2],[0,2]] = 1
print('a')