import imp
import cv2
from numpy import imag
from display import visualization
import numpy as np
import time
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
def image_processing(gray, crop_value, threadhold_value):
    start_time = time.time()
    crop_image = gray[crop_value[0][0]:crop_value[0][1], crop_value[1][0]:crop_value[1][1]]
    _, converted_image = cv2.threshold(crop_image, threadhold_value, 255, cv2.THRESH_BINARY)
    visualization.write_image('display', 'test_cut_line', converted_image)
    # converted_image = np.array(converted_image)
    pixel_list = np.argwhere(converted_image == 255)
    clustering = DBSCAN(eps=4, min_samples=30).fit(pixel_list)
#     first_array = np.take(pixel_list, (np.where(clustering.labels_ == 1)[0]), 0)
#     plt.scatter(pixel_list[:, 0], pixel_list[:, 1], 
#             s=1, cmap='inferno')
#     plt.scatter(first_array[:, 0], first_array[:, 1], c = '#ff7f0e',
#             s=1)
#     plt.show()
    end_time = time.time()
    print(end_time - start_time)