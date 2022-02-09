from tracemalloc import start
import cv2
from numpy import imag
from display import visualization
import numpy as np
import time
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from utils import check_string_width
def image_processing(image, crop_value, threadhold_value, head_tail_diff_ratio):
    start_time = time.time()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    crop_image = gray[crop_value[0][0]:crop_value[0][1], crop_value[1][0]:crop_value[1][1]]
    _, converted_image = cv2.threshold(crop_image, threadhold_value, 255, cv2.THRESH_BINARY)
    visualization.write_image('display', 'test_cut_line', converted_image)
    # converted_image = np.array(converted_image)
    pixel_list = np.argwhere(converted_image == 255)
    clustering = DBSCAN(eps=5, min_samples=30).fit(pixel_list)
    label = clustering.labels_
    end_time = time.time()
    print(end_time - start_time)
    print(crop_image.shape[0])
    for label_index in range(label.min(),label.max(),1):
        first_array = np.take(pixel_list, 
                        (np.where(label == label_index)[0]), 
                        0)
        x_list = first_array[:,0]
        x_max =  x_list.max() -  x_list.min()
        if x_max*1.5 > crop_image.shape[0]:
            # print(len(first_array[:,0]))
            collision, draw_points = check_string_width.get_side_size(first_array,head_tail_diff_ratio)
            if collision:
                start_point = tuple(np.array(draw_points[0])+ np.array([crop_value[1][0],crop_value[0][0]]))
                end_point = tuple(np.array(draw_points[-1])+ np.array([crop_value[1][0],crop_value[0][0]]))
                image = cv2.circle(image, start_point, 2, [0,255,255], 5)
    cv2.imshow('image', image)
    cv2.waitKey(0)
        # f =  open('testing_set/{}.npy'.format('first_array'), 'a') 
        # np.save('testing_set/{}.npy'.format('first_array'), first_array)
        # f.close()
        # plt.scatter(pixel_list[:, 0], 
        #         pixel_list[:, 1],
        #         c = clustering.labels_,
        #         s=1, cmap='inferno')
        # plt.scatter(first_array[:, 0], 
        #         first_array[:, 1], 
        #         c = '#FF0000',
        #         s=1)
        # # plt.show()
        # plt.pause(0.01)
        # plt.clf()
