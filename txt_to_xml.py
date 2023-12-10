#!/usr/bin/env python
#-*-coding:utf-8 -*-"
'''
@ Author: Onur Tosun
@ Create Time : 2023-11-29
@ Description : This script converts a CSV file
with bounding box annotations into the YOLO TXT format.
'''

import os
import argparse
from pathlib import Path
from PIL import Image
from xml.dom.minidom import Document

def write_xml(doc, image_name, width, height, objbud, class_dict):
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename_txt = doc.createTextNode(image_name)
    filename.appendChild(filename_txt)

    size = doc.createElement('size')
    annotation.appendChild(size)

    for size_elem, size_value in zip(['width', 'height'], [width, height]):
        size_coord = doc.createElement(size_elem)
        size.appendChild(size_coord)
        size_txt = doc.createTextNode(str(size_value))
        size_coord.appendChild(size_txt)

    depth = doc.createElement('depth')
    size.appendChild(depth)
    depth_txt = doc.createTextNode("3")
    depth.appendChild(depth_txt)

    for objbud_line in objbud:
        objbuds = objbud_line.split(' ')
        object_new = doc.createElement("object")
        annotation.appendChild(object_new)

        name = doc.createElement('name')
        object_new.appendChild(name)
        name_txt = doc.createTextNode(class_dict.get(objbuds[0], 'unknown'))
        name.appendChild(name_txt)

        bndbox = doc.createElement('bndbox')
        object_new.appendChild(bndbox)

        x1, y1, w1, h1 = map(float, objbuds[1:])
        coords = {'xmin': x1 - w1 / 2, 'ymin': y1 - h1 / 2, 'xmax': x1 + w1 / 2, 'ymax': y1 + h1 / 2}

        for coord_name, coord_value in coords.items():
            coord_elem = doc.createElement(coord_name)
            bndbox.appendChild(coord_elem)
            coord_txt = doc.createTextNode(str(int(coord_value * width)))
            coord_elem.appendChild(coord_txt)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="txt path")
    ap.add_argument("-img", "--image", required=True, help="images path")
    ap.add_argument("-o", "--output", required=True, help="output directory ")
    args = ap.parse_args()

    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    class_dict = {'0': "person"}

    annotations_path = Path(args.input)
    image_path = Path(args.image)

    for txt_file in annotations_path.glob("*.txt"):
        image_name = txt_file.stem + '.jpg'
        image_file_path = image_path / image_name

        im = Image.open(image_file_path)
        width, height = im.size

        with open(txt_file, "r") as filelabel:
            obj_lines = filelabel.read().split('\n')[:-1]

        xml_file_path = output_path / (txt_file.stem + '.xml')
        doc = Document()
        write_xml(doc, image_name, width, height, obj_lines, class_dict)

        with open(xml_file_path, "w") as f:
            f.write(doc.toprettyxml(indent='\t'))

if __name__ == "__main__":
    main()
