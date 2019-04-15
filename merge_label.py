import sys
import os
import os.path
import utils as util
# import time
# time1=time.time()

def MergeTxt(filepath, outfile):
    k = open(filepath+outfile, 'a+')    # create new file (1/2)
    k = open(filepath+outfile, 'r+')    # clear file contents (1/2)
    k.truncate()                        # clear file contents (2/2)

    # create new file's contenet (2/2)
    for parent, dirnames, filenames in os.walk(filepath):
        for filepath in filenames:
            txtPath = os.path.join(parent, filepath) 
            f = open(txtPath)
            k.write(f.read())
    print("Finished create merge file: ", parent + outfile)
    k.close()
    

if __name__ == '__main__':
    parent_path = "Labels/"
    child_path = util.label_path
    outfile  = "result.txt"

    try:
        for (i, filepath) in enumerate(child_path):
            filepath = os.path.join(parent_path, child_path[i]) 
            MergeTxt(filepath, outfile)
    except :
        print('There is an unexist folder!')

    # time2 = time.time()

