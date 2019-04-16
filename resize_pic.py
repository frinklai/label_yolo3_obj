from PIL import Image
import glob, os
import utils as util

dir_path_list  = util.label_path
file_type = '.jpg'

desire_ratio = 6

for (i, path) in enumerate(dir_path_list):
    for name in glob.glob('./Orig/' + dir_path_list[i] + '/*'):  
        orig_img = Image.open(name)
        img_name = os.path.split(name)[-1].split('.')[0]

        new_img_w = int(orig_img.size[0]/desire_ratio)
        new_img_h = int(orig_img.size[1]/desire_ratio)
        new_img = orig_img.resize((new_img_w, new_img_h))

        if (os.path.exists("./Train/" + dir_path_list[i])==False) :
            os.makedirs("./Train/" + dir_path_list[i])
        new_img.save("./Train/" + dir_path_list[i] + img_name + file_type)
        # print('new img:', [new_img.size[0], new_img.size[1]]   )
    print('['+str(i)+'] ' + "Save path : " +"./Train/" + dir_path_list[i] )




