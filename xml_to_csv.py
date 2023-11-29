#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ Author: Onur Tosun
@ Create Time: 2023-11-29
@ Description: This script converts an xml file
with bounding box annotations into the csv format.
'''
import glob
import argparse
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(xml_path):
    xml_list = []
    for xml_file in glob.glob(f"{xml_path}/*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        image = f"{xml_file.split('/')[-1].split('.')[0]}.jpg"
        for member in root.findall("object"):
            class_label = member[0].text
            value = (
                image,
                int(float(root.find("size")[0].text)),
                int(float(root.find("size")[1].text)),
                class_label,
                int(float(member[4][0].text)),
                int(float(member[4][1].text)),
                int(float(member[4][2].text)),
                int(float(member[4][3].text)),
            )
            xml_list.append(value)

    column_names = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]
    xml_df = pd.DataFrame(xml_list, columns=column_names)
    return xml_df

if __name__ == "__main__"

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Xmls path")
    ap.add_argument("-o", "--output", required=True, help="output file name")
    args = vars(ap.parse_args())

    xmls_path = args["input"]
    xml_df = xml_to_csv(xmls_path)
    xml_df.to_csv(args["output"], index=None)
    print(f"Successfully converted xml to csv. Your output file is {args['output']}")
