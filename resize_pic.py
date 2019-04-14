from PIL import Image
import glob, os

dir_path_list  = ['001', '002']
file_type = '.jpg'

for (i, path) in enumerate(dir_path_list):
    for name in glob.glob('./Orig/' + dir_path_list[i] + '/*'):  
        orig_img = Image.open(name)
        img_name = os.path.split(name)[-1].split('.')[0]
        out = orig_img.resize((640, 480))
        out.save("./Train/" + dir_path_list[i] + '/' + img_name + file_type)
    print('['+str(i)+'] ' + "Save path : " +"./Train/" + dir_path_list[i] )




