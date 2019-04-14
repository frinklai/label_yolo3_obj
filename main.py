#-------------------------------------------------------------------------------
# Name:        Object bounding box label tool
# Purpose:     Label object bboxes for ImageNet Detection data
# Author:      Qiushi
# Created:     06/06/2014
#
#-------------------------------------------------------------------------------
# from tkinter import *
# from tkinter.ttk import *
# import tkinter.messagebox

from __future__ import division
from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import glob
import random
import argparse
import resize_pic


parser = argparse.ArgumentParser()
# colors for the bboxes
COLORS = ['red', 'blue', 'yellow', 'pink', 'cyan', 'green', 'black']
# image sizes for the examples
SIZE = 256, 256

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("LabelTool")
        self.frame = Frame(self.parent)
        # self.frame.pack(fill=BOTH, expand=1)
        self.frame.pack()
        # self.parent.resizable(width = False, height = False)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None
        self.label_id = -1

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None

        # ----------------- GUI stuff ---------------------
        # self.parent.geometry('400x200')
        # dir entry & load
        self.label = Label(self.frame, text = "Image Dir:")
        self.label.grid(row = 0, column = 0,sticky = E)
        self.entry = Entry(self.frame, width=1)
        self.entry.grid(row = 0, column = 1, sticky = W+E)
        self.ldBtn = Button(self.frame, text = "Load", command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 2, sticky = W+E)


        self.label2 = Label(self.frame, text = "label_id:")
        self.label2.grid(row = 1, column = 0, sticky = E)
        self.entry2 = Entry(self.frame)
        self.entry2.grid(row = 1, column = 1, sticky = W+E)
        
        

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.cancelBBox)  # press <Espace> to cancel current bbox
        self.parent.bind("s", self.cancelBBox)
        self.parent.bind("a", self.prevImage) # press 'a' to go backforward
        self.parent.bind("d", self.nextImage) # press 'd' to go forward
        self.mainPanel.grid(row = 2, column = 1, rowspan = 20, sticky = W+N)

        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = 'Bounding boxes:')
        self.lb1.grid(row = 1, column = 2,  sticky = W+N)

        self.listbox = Listbox(self.frame, width = 22, height = 12)
        self.listbox.grid(row = 2, column = 2, sticky = N)

        self.btnDel = Button(self.frame, text = 'Save', command = self.saveImage)
        self.btnDel.grid(row = 3, column = 2, sticky = W+E+N)
        
        self.btnClear = Button(self.frame, text = 'ClearAll', command = self.clearBBox)
        self.btnClear.grid(row = 4, column = 2, sticky = W+E+N)

        

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 5, column = 1, columnspan = 2, sticky = W+E)

        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)

        

        # self.label3 = Label(self.frame, text = "Data")
        # self.label3.grid(row = 2, column = 0,sticky = E)
        # example pannel for illustration
        self.egPanel = Frame(self.frame, border = 10)
        self.egPanel.grid(row = 2, column = 0, rowspan = 5, sticky = N)
        self.tmpLabel2 = Label(self.egPanel, text = "Image:")
        self.tmpLabel2.pack(side = TOP, pady = 5)
        # self.egLabels = []
        # for i in range(3):
        #     self.egLabels.append(Label(self.egPanel))
        #     self.egLabels[-1].pack(side = TOP)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

    def loadDir(self, dbg = False):
        if not dbg:
            s = self.entry.get()
            self.parent.focus()
            self.category = int(s)
            
        else:
            s = r'D:\workspace\python\labelGUI'
        self.entry2.delete(0,END)
        self.entry2.insert(0,'')   
        self.imageDir = os.path.join(r'./Train', '%03d' %(self.category))

        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        if len(self.imageList) == 0:
            print('No .JPG images found in the specified dir!')
            return
        
        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

         # set up output dir
        self.outDir = os.path.join(r'./Labels', '%03d' %(self.category))
        
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        # load example bboxes
        # self.egDir = os.path.join(r'./Examples', '%03d' %(self.category))
        # if not os.path.exists(self.egDir):
        #     return
        # print("tag1")
        # filelist = glob.glob(os.path.join(self.egDir, '*.jpg'))

        # print("tag2")
        # self.tmp = []
        # self.egList = []
        # random.shuffle(filelist)
        # print("tag3")
        # for (i, f) in enumerate(filelist):
        #     if i == 3:
        #         break
        #     im = Image.open(f)
        #     r = min(SIZE[0] / im.size[0], SIZE[1] / im.size[1])
        #     new_size = int(r * im.size[0]), int(r * im.size[1])
        #     self.tmp.append(im.resize(new_size, Image.ANTIALIAS))
        #     self.egList.append(ImageTk.PhotoImage(self.tmp[-1]))
        #     self.egLabels[i].config(image = self.egList[-1], width = SIZE[0], height = SIZE[1])
        # print("tag4")
        self.loadImage()
        print('%d images loaded from %s' %(self.total, s))

    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 640), height = max(self.tkimg.height(), 530))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

        # load labels
        self.clearBBox()

        self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        labelname = self.imagename + '.txt'

        self.labelfilename = os.path.join(self.outDir, labelname)

        bbox_cnt = 0
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    bbox_cnt = str(line.strip())
                    info = bbox_cnt
                    tmp1 = os.path.split(info)[-1].split(' ')[1]
                    tmp2 = os.path.split(info)[-1].split(' ')[2]
                    tmp3 = os.path.split(info)[-1].split(' ')[3]
                    tmp4 = os.path.split(info)[-1].split(' ')[4]
                    # try:
                    #     tmp5 = self.entry2.get()
                    # except expression as identifier:
                    #     tmp5 = os.path.split(info)[-1].split(' ')[5]

                    if(self.entry2.get()==''):
                        tmp5 = os.path.split(info)[-1].split(' ')[5]
                    else:
                        tmp5 = self.entry2.get()
                    tmp = [tmp1, tmp2, tmp3, tmp4, tmp5]
                    print('info = ', tmp)
                    
                    self.bboxList.append(tuple(tmp))
                    # print("(self.bboxList[0]) = ", (self.bboxList[0]))
                    # print("len(self.bboxList[0]) = ", len(self.bboxList[0]))
                    # if(len(self.bboxList[0]) == 4):
                    #     self.bboxList[0] = [self.bboxList[0], self.label_id]
                    #     print("(self.bboxList[0]) = ", (self.bboxList[0]))
                    #     print("len(self.bboxList[0]) = ", len(self.bboxList[0]))
                    tmpId = self.mainPanel.create_rectangle(tmp[0], tmp[1], \
                                                            tmp[2], tmp[3], \
                                                            width = 2, \
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(END, '[%s]. (%s, %s) -> (%s, %s)' %(tmp5, tmp[0], tmp[1], tmp[2], tmp[3]) )
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
                        
    # def loadImage_orig(self):
    #     # load image
    #     imagepath = self.imageList[self.cur - 1]
    #     self.img = Image.open(imagepath)
    #     self.tkimg = ImageTk.PhotoImage(self.img)
    #     self.mainPanel.config(width = max(self.tkimg.width(), 640), height = max(self.tkimg.height(), 530))
    #     self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
    #     self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

    #     # load labels
    #     self.clearBBox()

    #     self.imagename = os.path.split(imagepath)[-1].split('.')[0]
    #     labelname = self.imagename + '.txt'

    #     self.labelfilename = os.path.join(self.outDir, labelname)

    #     bbox_cnt = 0
    #     if os.path.exists(self.labelfilename):
    #         with open(self.labelfilename) as f:
    #             for (i, line) in enumerate(f):
    #                 try:
    #                     if i == 0:
    #                         bbox_cnt = int(line.strip())
    #                         continue
    #                     tmp = [int(t.strip()) for t in line.split()]
    # ##                    print(tmp)
    #                     self.bboxList.append(tuple(tmp))
    #                     tmpId = self.mainPanel.create_rectangle(tmp[0], tmp[1], \
    #                                                             tmp[2], tmp[3], \
    #                                                             width = 2, \
    #                                                             outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
    #                     self.bboxIdList.append(tmpId)
    #                     self.listbox.insert(END, '(%d, %d) -> (%d, %d)' %(tmp[0], tmp[1], tmp[2], tmp[3]))
    #                     self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
    #                 except :
    #                     print('The label already replace complete.')

    def save_img_info(self):
        self.loadImage()
        self.saveImage()
        self.loadImage()
        elf.saveImage()

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write( (self.imageDir) +'.jpg ' )
            for bbox in self.bboxList:
                f.write(' '.join(map(str, bbox)) + '\n')
        print('[%s] Save image: %s.jpg complete!'  %(self.cur, self.imagename))


    def mouseClick(self, event):
        self.label_id = self.entry2.get()
        if self.STATE['click'] == 0:
            self.STATE['x'], self.STATE['y'] = event.x, event.y
        else:
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            self.bboxList.append((x1, y1, x2, y2, self.label_id))
            # self.bboxList.append((x1, y1, x2, y2))
            self.bboxIdList.append(self.bboxId)
            self.bboxId = None
            self.listbox.insert(END, '(%d, %d) -> (%d, %d)' %(x1, y1, x2, y2))
            self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
                                                            event.x, event.y, \
                                                            width = 2, \
                                                            outline = COLORS[len(self.bboxList) % len(COLORS)])

    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

if __name__ == '__main__':
    resize_pic
    parser.add_argument("-l",   dest='label_id', default=-1, type=int)
    label = parser.parse_args()

    if(label.label_id == -1):
        print("please enter label id\n")

    root = Tk()
    tool = LabelTool(root)
    tool.label_id = label.label_id
    print("Label_id is ", tool.label_id)
    
    root.resizable(width =  True, height = True)
    root.mainloop()
