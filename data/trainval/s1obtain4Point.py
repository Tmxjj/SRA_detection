# -*- coding: utf-8 -*-
from __future__ import division 
import os
import xml.dom.minidom
import cv2
import numpy as np
from PIL import Image  


def read_xml2img(ImgPath = 'data/trainval/images/', AnnoPath ='data/trainval/annfiles/', Savepath = 'data/trainval/4point_an'):

    imagelist = os.listdir(AnnoPath)
    output_txt = 'groundtruth.txt'  

    with open(output_txt, 'w') as f: 
        for image in imagelist:  
            image_pre, ext = os.path.splitext(image)
            imgfile = ImgPath + '/' + image_pre + '.jpg'
            xmlfile = AnnoPath + '/'  + image_pre + '.xml'
            im = cv2.imread(imgfile)
            DomTree = xml.dom.minidom.parse(xmlfile)
            annotation = DomTree.documentElement
            filenamelist = annotation.getElementsByTagName('filename')
            filename = filenamelist[0].childNodes[0].data
            objectlist = annotation.getElementsByTagName('object')

            print(filename)
            for objects in objectlist:
                namelist = objects.getElementsByTagName('name')
                objectname = namelist[0].childNodes[0].data
                rotated_bndbox = objects.getElementsByTagName('robndbox')  #robndbox rotated_bndbox
                #print(rotated_bndbox)
                for box in rotated_bndbox:
                        cx1 = box.getElementsByTagName('cx')
                        cx = int(float(cx1[0].childNodes[0].data))  # need int when showin in images
                        # print('cx = ', cx)
                        
                        cy1 = box.getElementsByTagName('cy')
                        cy = int(float(cy1[0].childNodes[0].data))
                        # print('cy = ', cy)
    
                        # cv2.rectangle(im,(xmin,ymin),(xmax,ymax), (0, 255, 0), 2)
                        w1 = box.getElementsByTagName('w')
                        w = int(float(w1[0].childNodes[0].data))
                        # print('w = ', w)
    
                        h1 = box.getElementsByTagName('h')
                        h = int(float(h1[0].childNodes[0].data))
                        # print('h = ', h)
    
                        theta1 = box.getElementsByTagName('angle')
                        theta = float(theta1[0].childNodes[0].data)
                        # print('theta = ', theta)


                        ang=theta+np.pi/2
                        c, s = np.sin(ang), np.cos(ang)
                        R = np.asarray([[c, s], [-s, c]])

                        # get 4 points
                        corners_original = np.array([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]], dtype=float)
                        R = np.asarray([[c, s], [-s, c]])
                        # 旋转角点  
                        rotated_corners = corners_original @ R.T  # 注意这里使用.T来获取R的转置  
                        # 平移到中心点  
                        translated_corners = rotated_corners + np.array([cx, cy])  
                        # 分配角点坐标到变量中  
                        x1, y1 = round(translated_corners[0, 0]), round(translated_corners[0, 1])  
                        x2, y2 = round(translated_corners[1, 0]), round(translated_corners[1, 1])  
                        x3, y3 = round(translated_corners[2, 0]), round(translated_corners[2, 1])  
                        x4, y4 = round(translated_corners[3, 0]), round(translated_corners[3, 1]) 

                        if x1<0 or x2<0 or x3<0 or x4<0 or y1<0 or y2<0 or y3<0 or y4<0:
                            print(xmlfile)
                        f.write(f'{image_pre}.jpg {max(int(x1),0)} {max(int(y1),0)} {max(int(x2),0)} {max(int(y2),0)} {max(int(x3),0)} {max(int(y3),0)} {max(int(x4),0)} {max(int(y4),0)} \n')


            # #input()   
            # path = Savepath + '/' + image_pre + '.jpg'
         
            # # input()
            # cv2.imwrite(path, im)
read_xml2img()