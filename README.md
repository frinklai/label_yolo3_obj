BBox-Label-Tool
===============

A simple tool for labeling object bounding boxes in images, implemented with Python Tkinter.
ref: https://github.com/puzzledqs/BBox-Label-Tool

Environment
----------
- python 3.5
- python PIL (Pillow)

Run
-------
$ python3 main.py


Data Organization
-----------------
LabelTool  
|  
|--main.py   *# source code for the tool*  
|  
|--Train/   *# Training data*  
|  
|--Labels/   *# Training data's label*  
|  
|--Orig/    *# The original img from maybe google, your camera and son on*  



Usage:
-----
**Step 0: cd /label_yolo3_obj**

**Step 1: Create needed folders (Orig, Train, Labels)**

**Step 2: Paste your original img data to "Orig" folder and classify them by folders**
  - About the rule of folder's name: 00id
  - eg. "001", "002", ..., "012" ... 
  - so the path will like: label_yolo3_obj/Orig/001 or label_yolo3_obj/Orig/012

**Step 3: edit "label_path" in utils.py**
  - eg. label_path = ['001/', '002/', ...]

**Step4: rename all datas in Orig folder**
  - Run python3 rename_file.py
  - You can still add new data and rename them, even you already train another original data. 
  - It is not needed to delete original data or do other operation.
  - Just paste new data and run rename_file.py

**Step 5: python3 main.py**
  - This program will generate training data with the size you set in resize_pic.py
  - Start to label your img and make labels
  - Run python3 main.py -r 0 
  - The arg -r 0 means program will ignore resize function

**Step 6: About the illustration of label tool UI**
  - Step 1. Type your folder id (1 for folder "001", 12 for folder "012") in "Image Dir"
  - Step 2. Click "Load" button to load one image.
  - Step 3. Start to label your img.
  - Step 4. Click "Next>>" button or key in "d" on keyboard to save info and load next img, until over.

**Step 7: python3 merge_label.py**
  - This will merge all of the label files that belong to same class to one file

**Other info:**
  - Click "Previous>>" button or key in "a" on keyboard  to save info and load previous img, until over.
  - Key in "esc" or "s" on keyboard  to cancel label.
  - Select the info you want to delete and click "Delete" button to delete bounding box info in list_box.
  - Click "ClearAll" button to clear all info in list_box.
  - Type desire photo number in "Go to Image No." and load it by click "Go" button

Illustration of label:
-----
Illustration of 00X.txt in "Labels" folder: path, x1, y1, x2, y2, label_id
