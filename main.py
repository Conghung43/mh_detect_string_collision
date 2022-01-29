from ast import literal_eval
import cv2
from initiation import init_config
from matplotlib import pyplot as plt
from collections import Counter
from scipy.signal import find_peaks
import time
import numpy as np
system_config = init_config.get_config_data()
image = cv2.imread('testing_set\IMG_1068.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
heigh, width = gray.shape
pattent_xaxis_list = literal_eval(system_config['program']['pattent_xaxis_list'])
pattent_yaxis_list = literal_eval(system_config['program']['pattent_yaxis_list'])

for pattent_xaxis in pattent_xaxis_list:
    s_time= time.time()
    start_left = int(pattent_yaxis_list[0]*width)
    end_right = int(pattent_yaxis_list[1]*width)
    data_list = gray[int(pattent_xaxis*heigh)][start_left:end_right]
    
    peaks, _ = find_peaks(data_list, height=100, distance= 10)
    # peaks = list(np.asarray(peaks) + start_left-1)
    e_time = time.time()
    print(e_time - s_time)
    # count_dict = Counter(data_list)
    # plt.plot(list(range(start_left, end_right)),data_list)
    plt.plot(list(range(0, len(data_list))),data_list)
    plt.plot(peaks, data_list[peaks], "x")
    # plt.plot([1]*len(data_list),data_list)
    # plt.plot(list(count_dict.keys()),list(count_dict.values()))
    plt.pause(3)
    plt.clf()
plt.show()