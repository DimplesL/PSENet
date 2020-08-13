import json
import codecs
import cv2
import os
import matplotlib.pyplot as plt
import pandas as pd
from common import *

gt_file = '/Users/qiuyurui/Desktop/Text-Detect-Data/train_full_labels.json'
img_dir = '/Users/qiuyurui/Desktop/Text-Detect-Data/train_full_images'
save_dir = '/Users/qiuyurui/Desktop/Text-Detect-Data/train_full_images'

gt_json = json.load(open(gt_file, 'r'))
defult_shape = {
    "label": "",
    "line_color": None,
    "fill_color": None,
    "points": [
    ],
    "shape_type": "polygon"
}
print(len(gt_json))
# file_names = list(gt_json.keys())
ratios = []
for file_name, content in gt_json.items():
    print(file_name)
    shapes = []
    img = cv2.imread(os.path.join(img_dir, file_name + '.jpg'))
    h_o, w_o = img.shape[:2]
    for cont in content:
        ratio = round(abs(polygon_area(cont['points'])) / (h_o * w_o), 8)
        if cont['illegibility'] is False:
            if ratio <= 0.0014:
                label = 'text_5'
            if ratio <= 0.0005:
                label = 'text_4'
            if ratio <= 0.0002:
                label = 'text_3'
            if ratio <= 0.00012:
                label = 'text_2'
            else:
                label = 'text_0'
        else:
            label = 'text_1'

        ratios.append(ratio)
        shape = defult_shape.copy()
        shape['label'] = label
        shape['points'] = cont['points']
        shape['ratio'] = ratio
        shapes.append(shape)

    create_json_label(file_name + '.jpg', save_dir, h_o, w_o, shapes)
#
# with open('s.txt', 'w') as f:
#     f.write(str(ratios))
