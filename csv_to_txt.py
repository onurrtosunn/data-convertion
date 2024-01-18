#!/usr/bin/env python
#-*-coding:utf-8 -*-"
'''
@ Author: Onur Tosun
@ Create Time : 2023-11-29
@ Description : This script converts a CSV file
with bounding box annotations into the YOLO TXT format.
'''
import os 
import glob 
import argparse
import pandas as pd
from pandas.core.algorithms import unique

def convert_coordinates(size, box):
    """
    Converts coordinates from relative to absolute values
    """
    dw = 1.0/size[0]
    dh = 1.0/size[1]

    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def csv_to_txt(csv_path ,out_path):
    """
    Convert CSV file with bounding boxes to txt file for YOLO format
    """
    df = pd.read_csv(csv_path)
    unique_classes = pd.unique(df['class'])
    labels = {}

    for i,label in enumerate(unique_classes):
        labels[label]=i
    print(labels)
    
    for name, group in df.groupby('filename'):  
        if name.endswith("jpg"):  
            txt_filename = os.path.join(out_path, name + '.txt')
            with open(txt_filename, "w") as f:
                for row_index, row in group.iterrows():
                    xmin = row['xmin']
                    ymin = row['ymin']
                    xmax = row['xmax']
                    ymax = row['ymax']
                    width = row['width']
                    height = row['height']
                    label = row['class']

                    label_str = str(labels[label])
                    values = (float(xmin), float(xmax), float(ymin), float(ymax))

                    bounding_box_values = convert_coordinates((width,height), values)
                    f.write(label_str + " " + " ".join([("%.6f" % i) for i in bounding_box_values]) + '\n')

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input_dir", required=True, help="csv path")
    ap.add_argument("-o", "--output_dir", required=True, help="output directory ")
    args = vars(ap.parse_args())   

    if not os.path.exists(args["output_dir"]):
       os.makedirs(args["output_dir"])   
    csv_to_txt(args["input_dir"] , args["output_dir"])   
