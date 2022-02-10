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
    crop_image_color = gray[crop_value[0][0]:crop_value[0][1], crop_value[1][0]:crop_value[1][1]]
    # crop_image_resize = cv2.resize(crop_image_color, (int(crop_image_color.shape[1]/2), int(crop_image_color.shape[0]/2)), interpolation = cv2.INTER_AREA)
    _, converted_image = cv2.threshold(crop_image, threadhold_value, 255, cv2.THRESH_BINARY)
    # cv2.imshow('image', converted_image)
    # cv2.waitKey(0)
    visualization.write_image('display', 'test_cut_line', converted_image)
    # converted_image = np.array(converted_image)
    pixel_list = np.argwhere(converted_image == 255)
    clustering = DBSCAN(eps=5, min_samples=30).fit(pixel_list)
    label = clustering.labels_
    end_time = time.time()
    print(end_time - start_time)
    # return
    # print(crop_image.shape[0])
    for label_index in range(label.min(),label.max(),1):
        first_array = np.take(pixel_list, 
                        (np.where(label == label_index)[0]), 
                        0)
        x_list = first_array[:,0]
        x_max =  x_list.max() -  x_list.min()
        if x_max*1.5 > crop_image.shape[0]:
            # continue
            collision, draw_points = check_string_width.get_side_size(first_array,head_tail_diff_ratio)
            if collision:
                print(label_index)
                start_point = np.array(draw_points[0])+ np.array([crop_value[0][0],crop_value[1][0]])
                # end_point = tuple(np.array(draw_points[-1])+ np.array([crop_value[1][0],crop_value[0][0]]))
                image = cv2.circle(image, (start_point[1],start_point[0]), 2, [0,255,255], 5)

                # crop_image_color = cv2.circle(crop_image_color, (draw_points[0][1],draw_points[0][0]), 2, [0,255,255], 5)

                cv2.imshow('image', image)
                cv2.waitKey(0)
        # f =  open('testing_set/{}.npy'.format('first_array'), 'a') 
        # np.save('testing_set/{}.npy'.format('first_array'), first_array)
        # f.close()
                # plt.scatter(pixel_list[:, 0], 
                #         pixel_list[:, 1],
                #         c = clustering.labels_,
                #         s=1, cmap='inferno')
                # # plt.scatter(first_array[:, 0], 
                # #         first_array[:, 1], 
                # #         c = '#FF0000',
                # #         s=1)
                # plt.plot(first_array[:, 0][0],first_array[:, 1][0],marker="o", color="red")
                # # plt.show()
                # plt.pause(1)
                # plt.clf()


    plt.scatter(pixel_list[:, 1], 
            pixel_list[:, 0],
            s=1, cmap='inferno')
    plt.show()