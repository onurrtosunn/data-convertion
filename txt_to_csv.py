#!/usr/bin/env python
#-*-coding:utf-8 -*-"
'''
@ Author: Onur Tosun
@ Create Time : 2023-12-13
@ Description : This script converts a txt file
with bounding box annotations into the CSV format.
'''

import os
import argparse
import pandas as pd
from PIL import Image

def read_labels(file_path):
    with open(file_path, "r", encoding="ISO-8859-1") as file:
        lines = file.read().split('\n')
        return lines[:len(lines)-1]


def convert_annotations(annotations, img_size, dict):
    w, h = img_size
    converted_annotations = []

    for annotation in annotations:
        obj_parts = annotation.split(' ')
        try:
            class_name = dict[obj_parts[0]]
        except KeyError as e:
            print(f"Error: {e}. obj_parts[0]: {obj_parts[0]}")
            continue
        x1, y1, w1, h1 = map(float, obj_parts[1:])
        
        xmin = int((x1 * w) - (w1 * w) / 2.0)
        ymin = int((y1 * h) - (h1 * h) / 2.0)
        xmax = int((x1 * w) + (w1 * w) / 2.0)
        ymax = int((y1 * h) + (h1 * h) / 2.0)

        converted_annotations.append([class_name, xmin, ymin, xmax, ymax])

    return converted_annotations

def write_to_csv(ann_path, img_path, output_path, dict):
    annotations = []

    for root, dirs, files in os.walk(ann_path):
        for file in files:
            img_name = os.path.splitext(file)[0] + '.jpg'
            img_path = os.path.join(img_path, img_name)
            
            with Image.open(img_path) as img:
                img_size = img.size

            labels = read_labels(os.path.join(ann_path, file))
            converted_annotations = convert_annotations(labels, img_size, dict)
            
            for annotation in converted_annotations:
                annotations.append([img_name, *img_size, *annotation])

    column_names = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    df = pd.DataFrame(annotations, columns=column_names)
    df.to_csv(output_path, index=None)
    print(annotations[:10])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input txt path")
    parser.add_argument("-img", "--image", required=True, help="input images path")
    parser.add_argument("-o", "--output", required=True, help="output csv path")
    args = parser.parse_args()

    class_dict = {'0': 'class1', '1': 'class2', '2': 'class3', '3': 'class4'}

    write_to_csv(args.input, args.image, args.output, class_dict)
