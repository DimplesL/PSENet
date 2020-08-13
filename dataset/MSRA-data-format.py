# coding:utf-8

import os
import cv2
import json
from common import *

dst_dir = '/Users/qiuyurui/Desktop/Text-Detect-Data/MSRA-TD500/test/'
save_dir = '/Users/qiuyurui/Desktop/Text-Detect-Data/MSRA-TD500/test/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

defult_shape = {
    "label": "",
    "line_color": None,
    "fill_color": None,
    "points": [
    ],
    "shape_type": "polygon"
}
ratios = []
for fileName in os.listdir(dst_dir):

    fname = dst_dir + fileName
    if fname.endswith(".gt"):
        print(fname)
        f = open(fname, 'r')
        savestr = ''
        img = cv2.imread(fname.replace('gt', 'jpg'))
        h_o, w_o = img.shape[:2]
        shapes = []
        for line in f:
            shape = defult_shape.copy()
            line = line.strip()
            line = line.split(' ')
            line = list(map(float, line))  # MSRA-TD500 gt
            # line = list(map(float, line[0:6]))   # HUST-TR400 gt
            difficult = int(line[1])

            x, y = line[2], line[3]
            w, h = line[4], line[5]
            ratio = round(w * h / (h_o * w_o), 4)
            ratios.append(ratio)
            # print(difficult, ratio)
            # centralx=x+w/2
            # centraly = y + h / 2
            # points = [x, y, x, y + h, x + w, y + h, x + w, y]
            pointsrotate = rec_rotate(x, y, w, h, line[-1])
            if difficult is 0:
                if ratio <= 0.0007:
                    label = 'text_5'
                if ratio <= 0.0005:
                    label = 'text_4'
                if ratio <= 0.0002:
                    label = 'text_3'
                if ratio <= 0.0001:
                    label = 'text_2'
                else:
                    label = 'text_0'
            else:
                label = 'text_1'
            shape['label'] = label
            shape['points'] = [[int(pointsrotate[0]), int(pointsrotate[1])],
                               [int(pointsrotate[2]), int(pointsrotate[3])],
                               [int(pointsrotate[4]), int(pointsrotate[5])],
                               [int(pointsrotate[6]), int(pointsrotate[7])]]
            shape['ratio'] = ratio
            shapes.append(shape)
            boxstr = str(int(pointsrotate[0])) + ',' + str(int(pointsrotate[1])) + ',' + str(
                int(pointsrotate[2])) + ',' + str(int(pointsrotate[3])) + ',' + str(int(pointsrotate[4])) + ',' + str(
                int(pointsrotate[5])) + ',' + str(int(pointsrotate[6])) + ',' + str(
                int(pointsrotate[7]))
            # savestr = savestr + boxstr + ',' + 'text_{}\n'.format(difficult)

            draw_box(img, boxstr + ',' + 'text_{}_{}\n'.format(difficult, ratio))
        # cv2.imshow('show', img)
        # cv2.waitKey(0)
        create_json_label(fileName.replace('gt', 'jpg'), save_dir, h_o, w_o, shapes)
        # savename = save_dir + fileName.split(".")[0] + '.txt'
        # savef = open(savename, 'w')
        # savef.write(savestr)
        # savef.close()
# with open('s.txt', 'w+') as f:
#     f.write(str(ratios))

# 原文链接：https://blog.csdn.net/qq_36756866/java/article/details/105652368
