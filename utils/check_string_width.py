import numpy as np

f =  open('testing_set/{}.npy'.format('first_array'), 'rb')
string_pixel_list = np.load(f, allow_pickle=True)
diff_ratio = 1.5

# def main(string_pixel_list, diff_ratio):

def head_tail_size_comparision(first_size, second_side, diff_ratio):
    if first_size > second_side:
        two_side_ratio = first_size/second_side
    else:
        two_side_ratio = second_side/first_size
    if two_side_ratio > diff_ratio:
        return False
    else:
        return True
def get_side_size(string_pixel_list, switch_side):
    x_list = string_pixel_list[:,0]
    y_list = string_pixel_list[:,1]
    if x_list.max() > y_list.max():
        

# def check3point():
