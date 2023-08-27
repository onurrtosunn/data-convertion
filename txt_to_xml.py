"""
Usage : python txt_to_xml.py -input /input/txt/path/ -output output/xml/path
"""
import os
import os.path
import argparse
from PIL import Image
from xml.dom.minidom import Document


def write_xml(tmp, image_name, w, h, objbud, wxml, dict):

    doc = Document()
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename_txt = doc.createTextNode(image_name)
    filename.appendChild(filename_txt)

    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder_txt = doc.createTextNode(wxml)
    folder.appendChild(folder_txt)  

    size = doc.createElement('size')
    annotation.appendChild(size)

    width = doc.createElement('width')
    size.appendChild(width)
    width_txt = doc.createTextNode(str(w))
    width.appendChild(width_txt)

    height = doc.createElement('height')
    size.appendChild(height)
    height_txt = doc.createTextNode(str(h))
    height.appendChild(height_txt)

    depth = doc.createElement('depth')
    size.appendChild(depth)
    depth_txt = doc.createTextNode("3")
    depth.appendChild(depth_txt)

    
    for i in range(0, int(len(objbud))):
        objbuds=objbud[i].split(' ')
        object_new = doc.createElement("object")
        annotation.appendChild(object_new)

        name = doc.createElement('name')
        object_new.appendChild(name)
        name_txt = doc.createTextNode(dict[objbuds[0]])
        name.appendChild(name_txt)

        bndbox = doc.createElement('bndbox')
        object_new.appendChild(bndbox)
        
        x1 = float(objbuds[1])
        y1 = float(objbuds[2])
        w1 = float(objbuds[3])
        h1 = float(objbuds[4])
        
        xmin = doc.createElement('xmin')
        bndbox.appendChild(xmin)
                    
        xmin_txt2 = int((x1*w) - (w1*w)/2.0)
        xmin_txt = doc.createTextNode(str(xmin_txt2))
        xmin.appendChild(xmin_txt)

        ymin = doc.createElement('ymin')
        bndbox.appendChild(ymin)
        ymin_txt2 = int((y1*h)-(h1*h)/2.0)
        ymin_txt = doc.createTextNode(str(ymin_txt2))
        ymin.appendChild(ymin_txt)

        xmax = doc.createElement('xmax')
        bndbox.appendChild(xmax) 
        xmax_txt2 = int((x1*w)+(w1*w)/2.0)
        xmax_txt = doc.createTextNode(str(xmax_txt2))
        xmax.appendChild(xmax_txt)

        ymax = doc.createElement('ymax')
        bndbox.appendChild(ymax)
        ymax_txt2 = int((y1*h)+(h1*h)/2.0)
        ymax_txt = doc.createTextNode(str(ymax_txt2))
        ymax.appendChild(ymax_txt)

    tempfile = tmp + "test.xml"
    with open(tempfile, "w") as f:
        f.write(doc.toprettyxml(indent='\t'))

    rewrite = open(tempfile, "r")
    lines = rewrite.read().split('\n')
    newlines = lines[1:len(lines) - 1]
    fw = open(wxml, "w")
    for i in range(0, len(newlines)):
        fw.write(newlines[i] + '\n')

    fw.close()
    rewrite.close()
    os.remove(tempfile)
    return


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="txt path")
    ap.add_argument("-img", "--image", required=True, help="images path")
    ap.add_argument("-o", "--output", required=True, help="output directory ")
    args = vars(ap.parse_args()) 

    if not os.path.exists(args["output"]):
        os.mkdir(args["output"])

    dict = {'0': "class1",
            '1': "class2",}     

    annotations_path = args["input"]
    image_path = args["image"]
    xml_path = args["output"]

    for files in os.walk(annotations_path):
        temp = './temp/'
        if not os.path.exists(temp):
            os.mkdir(temp)

        for file in files[2]:
            # Read image and get its size attributes
            image_name = os.path.splitext(file)[0] + '.jpg'
            image_file_path = image_path + image_name
            
            im = Image.open(image_file_path)
            width = int(im.size[0])
            height = int(im.size[1])
            
            filelabel = open(annotations_path + file, "r")
            lines = filelabel.read().split('\n')
            obj = lines[:len(lines)-1]
            filename = xml_path + os.path.splitext(file)[0] + '.xml'
            write_xml(temp, image_name, width, height, obj, filename, dict)
        os.rmdir(temp)