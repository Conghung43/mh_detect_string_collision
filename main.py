from ast import literal_eval
import string
from webbrowser import get
import cv2
from initiation import init_config
from collections import Counter
import time
import numpy as np
import utils.find_white_string as find_white_string
import utils.measure_string_width as measure_string_width
from display import main_display
import string_class
from utils import new_point_verify
from utils import get_white_pixel_postition
def append_new_string(string_property,peak_pixel, string_width):
    string_property.append(string_class.WhiteString())
    string_property[-1].set(peak_pixel,
                            string_width)
    return string_property

system_config = init_config.get_config_data()
image = cv2.imread('testing_set/IMG_1068.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
heigh, width = gray.shape
pattent_xaxis_list = (np.array(literal_eval(system_config['program']['pattent_xaxis_list']))*heigh).astype(int)
pattent_xaxis_frame = (np.array(literal_eval(system_config['program']['pattent_xaxis_frame']))*heigh).astype(int)
pattent_yaxis_list = (np.array(literal_eval(system_config['program']['pattent_yaxis_list']))*width).astype(int)
threadhold_from_peak = int(system_config['program']['threadhold_from_peak'])
peak_distance = int(system_config['program']['peak_distance'])
default_value = int(system_config['program']['default_value'])
valid_angle = int(system_config['program']['valid_angle'])
s_time= time.time()
string_property = []
for pattent_xaxis in pattent_xaxis_list:
    main_display.draw_cut_line(image, pattent_xaxis,[0,255,0])
    data_list = gray[pattent_xaxis][pattent_yaxis_list[0]:pattent_yaxis_list[1]]
    average_threadhold, peak_pixel = find_white_string.get_string_property(data_list,
                                            threadhold_from_peak, 
                                            peak_distance,
                                            pattent_yaxis_list[0])
    # main_display.show_gray_image_threadhold(gray, average_threadhold)
    get_white_pixel_postition.image_processing(gray, (pattent_xaxis_frame, pattent_yaxis_list), average_threadhold)
    string_width_list = measure_string_width.measure_string_width(data_list, 
                                            average_threadhold)
    # Based on tracking
    temp_array = [len(peak_pixel),len(string_width_list)]
    len_loop = temp_array[np.argsort(temp_array)[0]]
    if len(string_property) == 0:
        for index in range(len_loop):
            string_property = append_new_string(string_property, 
                                    (peak_pixel[index],pattent_xaxis),
                                    string_width_list[index])
            # string_property.append(string_class.WhiteString())
            # string_property[-1].set((peak_pixel[index],pattent_xaxis),
            #                         string_width_list[index])
    else:
        for index in range(len_loop):
            if index >= len(string_property):
                string_property = append_new_string(string_property, 
                                        (peak_pixel[index],pattent_xaxis),
                                        string_width_list[index])
                continue
            current_index_distance = abs(peak_pixel[index]-string_property[index].get(-1)[0][0])
            if index > 0: 
                previous_index_distance = abs(peak_pixel[index]-string_property[index-1].get(-1)[0][0])
            else: 
                previous_index_distance = default_value
            if index < len(string_property)-1:
                next_index_distance = abs(peak_pixel[index]-string_property[index+1].get(-1)[0][0])
            else:
                next_index_distance = default_value

            distance_list = [previous_index_distance, current_index_distance, next_index_distance]
            sorted_index = np.argsort(distance_list)
            target_index = index - (sorted_index[0] - 1)
            if target_index >= len(string_property):
                string_property = append_new_string(string_property, 
                                        (peak_pixel[index],pattent_xaxis),
                                        string_width_list[index])
                continue
            lastest_point_position = string_property[target_index].get(-1)[0]
            new_point_position = (peak_pixel[index],pattent_xaxis)
            #Check new point position by angle
            if new_point_verify.angle_verify(lastest_point_position, new_point_position, valid_angle):
                string_property[target_index].set(new_point_position, 
                                            string_width_list[index])
main_display.draw_detected_white_line(image, string_property)
e_time = time.time()
print(e_time - s_time)
