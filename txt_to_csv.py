"""
Usage : python txt_to_csv.py -input /input/txt/path/ -output output/csv/path
"""

import os
import os.path
import argparse
import pandas as pd
from PIL import Image
from xml.dom.minidom import Document


def write_to_csv(ann_path ,img_path ,dict):
    
    annotations = []
    for files in os.walk(ann_path):
        for file in files[2]:

            # Read image and get its size attributes
            img_name = os.path.splitext(file)[0] + '.jpg'
            fileimgpath = os.path.join(img_path ,img_name)
            im = Image.open(fileimgpath)
            w = int(im.size[0])
            h = int(im.size[1])

            filelabel = open(os.path.join(ann_path , file), "r")
            lines = filelabel.read().split('\n')
            obj = lines[:len(lines)-1]  
            
            for i in range(0, int(len(obj))):
                objbud=obj[i].split(' ')                
                name = dict[objbud[0]]
                x1 = float(objbud[1])
                y1 = float(objbud[2])
                w1 = float(objbud[3])
                h1 = float(objbud[4])

                xmin = int((x1*w) - (w1*w)/2.0)
                ymin = int((y1*h) - (h1*h)/2.0)
                xmax = int((x1*w) + (w1*w)/2.0)
                ymax = int((y1*h) + (h1*h)/2.0)

                annotations.append([img_name ,w ,h ,name ,xmin ,ymin ,xmax ,ymax])
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax' ]
    df = pd.DataFrame(annotations, columns=column_name)        
    print(annotations[:10])
    return df

if __name__ == "__main__" :

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="input txt path")
    ap.add_argument("-img", "--image", required=True, help="input images path")
    ap.add_argument("-o", "--output", required=True, help="output csv path ")
    args = vars(ap.parse_args()) 

    dict = {'0' : 'class1',
            '1': "class2"}      
    
    ann_path = args["input"]
    img_path = args["image"]
    csv_path = args["output"]  

    data=write_to_csv(ann_path ,img_path  ,dict)      
    data.to_csv(csv_path, index=None)
