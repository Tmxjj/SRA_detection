import xml.etree.ElementTree as ET
import math
import numpy as np
import os 
from tqdm import tqdm
# 解析robndbox并转换为DOTA格式
def robndbox_to_dota(cx, cy, w, h, angle):
    ang = angle+np.pi/2 # DOTA中角度为逆时针
  
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

    # angle_rad = math.radians(angle_rad)
    

    # dx = w / 2
    # dy = h / 2

    # x1 = cx + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
    # y1 = cy + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)

    # x2 = cx - dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
    # y2 = cy - dx * math.sin(angle_rad) + dy * math.cos(angle_rad)

    # x3 = cx - dx * math.cos(angle_rad) + dy * math.sin(angle_rad)
    # y3 = cy - dx * math.sin(angle_rad) - dy * math.cos(angle_rad)

    # x4 = cx + dx * math.cos(angle_rad) + dy * math.sin(angle_rad)
    # y4 = cy + dx * math.sin(angle_rad) - dy * math.cos(angle_rad)
    return [max(int(x1),0), max(int(y1),0), 
            max(int(x2),0), max(int(y2),0), 
            max(int(x3),0), max(int(y3),0), 
            max(int(x4),0), max(int(y4),0)]


# 解析XML文件
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)
    
    objects = []

    for obj in root.findall('object'):
        name = obj.find('name').text
        difficult = int(obj.find('difficult').text)

        robndbox = obj.find('robndbox')
        cx = float(robndbox.find('cx').text)
        cy = float(robndbox.find('cy').text)
        w = float(robndbox.find('w').text)
        h = float(robndbox.find('h').text)
        angle = float(robndbox.find('angle').text)

        coords = robndbox_to_dota(cx, cy, w, h, angle)
        objects.append(coords + [name, difficult])

    return objects

# 将数据保存为DOTA格式文件
def save_to_dota(objects, output_file):
    with open(output_file, 'w') as f:
        for obj in objects:
            line = ",".join(map(str, obj))
            f.write(line + '\n')
def mian():
    output_folder = 'data/trainval/dota_annfiles'
    input_folder = 'data/trainval/annfiles'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    annfile_list = os.listdir(input_folder)
    for annfile in annfile_list:  
            image_pre, ext = os.path.splitext(annfile)
            print(image_pre)
            xml_file = input_folder + '/' + image_pre + '.xml'
            txt_file = output_folder + '/'  + image_pre + '.txt'
            objects = parse_xml(xml_file)
            save_to_dota(objects, txt_file)

mian()


