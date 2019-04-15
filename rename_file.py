import sys
import os
import os.path
import utils as util


def sort_list(j):
    if(j>=0 and j<=9):
        n=2
    elif (j>=10 and j<=99):
        n=1
    elif (j>=100 and j<=999):
        n=0
    else:
        print('too many image data, more than 1000.')
    return n

if __name__ == '__main__':
    file_type = '.jpg'
    parent_file_path = './Orig/'
    child_file_path = util.label_path
    new_name_list = ['tea_', 'soda_']
    old_data_num = 0
    
    try:
        for i,item in enumerate(child_file_path):
            old_data_num = 0
            new_data_num = 0
            file_path = parent_file_path + item
            file_name_list = os.listdir(file_path)
            file_name_list.sort()

            for (j, file_name) in enumerate(file_name_list):
                if(new_name_list[i] in file_name):
                    old_data_num+=1
                else:
                    new_data_num+=1
                    rand_name = 'zzz_'+str(new_data_num)
                    os.rename(file_path+file_name, file_path+rand_name)

            print('old_data_num = ', old_data_num)
            file_name_list = os.listdir(file_path)
            file_name_list.sort()
            # 
            
            for (j, file_name) in enumerate(file_name_list):
                if(j < old_data_num):
                    continue
                print([j, old_data_num])
                redun_0 = '0' * sort_list(j)
                new_name = (new_name_list[i] + redun_0 + str(j) + file_type)

                old_name = file_path + file_name
                new_name = file_path + new_name
                os.rename(old_name, new_name)
    except:
        print('no such folder:', parent_file_path+item)






