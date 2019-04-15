import sys
import os
import os.path
import utils as util
# import time
# time1=time.time()

if __name__ == '__main__':
    file_type = '.jpg'
    parent_file_path = './Orig/'
    child_file_path = util.label_path
    new_name_list = ['tea_', 'soda_']

    for i,item in enumerate(child_file_path):
        try:
            file_path = parent_file_path + item
            file_name_list = os.listdir(file_path)
            for (j, file_name) in enumerate(file_name_list):
                new_name = new_name_list[i]
                new_name = (new_name + str(j) + file_type)
                os.rename(file_path+file_name, file_path+new_name)
        except:
            print('no such folder:', parent_file_path+item)
        
        # file_path = parent_file_path + item
        # file_name_list = os.listdir(file_path)
        # for (j, file_name) in enumerate(file_name_list):
        #     new_name = new_name_list[i]
        #     new_name = (new_name + str(j) + file_type)
        #     print([file_path+file_name, file_path+new_name] )





