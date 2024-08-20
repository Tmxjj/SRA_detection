import numpy as np
ann_file = 'data/trainval/dota_annfiles/1.txt'
with open(ann_file) as f:
        s = f.readlines()
        for si in s:
            bbox_info = si.split(',')
            poly = np.array(bbox_info[:8], dtype=np.float32)