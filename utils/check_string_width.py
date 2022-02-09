from cv2 import rectify3Collinear
from matplotlib.pyplot import xlim
import numpy as np

# f =  open('testing_set/{}.npy'.format('first_array'), 'rb')
# string_pixel_list = np.load(f, allow_pickle=True)
# diff_ratio = 1.5
# string_default_width = 10
# def main(string_pixel_list, diff_ratio):

def head_tail_size_comparision(ratio_list, diff_ratio):
    first_size, second_side = ratio_list
    big_side = 0
    if first_size > second_side:
        two_side_ratio = first_size/second_side
    else:
        two_side_ratio = second_side/first_size
        big_side = 1
    print(two_side_ratio)
    if two_side_ratio > diff_ratio:
        return True, big_side
    else:
        return False, big_side
def get_side_size(string_pixel_list, head_tail_diff_ratio):
    x_list = string_pixel_list[:,0]
    y_list = string_pixel_list[:,1]
    x_max =  x_list.max() -  x_list.min()
    y_max =  y_list.max() -  y_list.min()
    if x_max > y_max:
        ratio_list = []
        for index in range(2):
            three_position = []
            for three_pos_index in range(2):
                if index == 0:
                    min_x_side = x_list.min() + int((three_pos_index + 1)*y_max/4)
                    three_position.append(min_x_side)
                else:
                    max_x_size =x_list.max() - int((three_pos_index + 1)*y_max/4)
                    three_position.append(max_x_size)
            ratio_list.append(check3point(string_pixel_list,three_position, 0))
        collision, biger_side = head_tail_size_comparision(ratio_list, head_tail_diff_ratio)
        draw_point = []
        if collision:
            print(ratio_list)
            if biger_side == 0:
                draw_point = [[min_x_side, y_pos] for y_pos in np.where(string_pixel_list[:,0]==min_x_side)[0]]
            else:
                draw_point = [[max_x_size, y_pos] for y_pos in np.where(string_pixel_list[:,0]==max_x_size)[0]]
    return collision, draw_point

def check3point(string_pixel_list,three_position, element_index):
    string_width = 0
    for position in three_position:
        string_width = string_width + len(np.where(string_pixel_list[:,element_index] == position)[0])
    return int(string_width/len(three_position))
# get_side_size(string_pixel_list, False)