import math
import os
import json
import codecs
import cv2
import numpy as np


def draw_box(img, box_str):
    points = box_str.split(',')
    if len(points) >= 9:
        point1_x = int(points[0])
        point1_y = int(points[1])
        point2_x = int(points[2])
        point2_y = int(points[3])
        point3_x = int(points[4])
        point3_y = int(points[5])
        point4_x = int(points[6])
        point4_y = int(points[7])
        label = points[8].strip()
        cv2.line(img, (point1_x, point1_y), (point2_x, point2_y), (255, 0, 0), 3)
        cv2.line(img, (point2_x, point2_y), (point3_x, point3_y), (0, 255, 0), 3)
        cv2.line(img, (point3_x, point3_y), (point4_x, point4_y), (0, 0, 255), 3)
        cv2.line(img, (point4_x, point4_y), (point1_x, point1_y), (0, 255, 255), 3)
        cv2.putText(img, label, (point1_x, point1_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (125, 125, 0), 2)
    return img


def vector_product(coord):
    coord = np.array(coord).reshape((4, 2))
    temp_det = 0
    for idx in range(3):
        temp = np.array([coord[idx], coord[idx + 1]])
        temp_det += np.linalg.det(temp)
    temp_det += np.linalg.det(np.array([coord[-1], coord[0]]))
    return temp_det * 0.5


def cal_distance(point1, point2):
    dis = np.sqrt(np.sum(np.square(point1[0] - point2[0]) + np.square(point1[1] - point2[1])))
    return dis


# 基于海伦公式计算不规则四边形的面积
def helen_formula(coord):
    coord = np.array(coord).reshape((4, 2))
    # 计算各边的欧式距离
    dis_01 = cal_distance(coord[0], coord[1])
    dis_12 = cal_distance(coord[1], coord[2])
    dis_23 = cal_distance(coord[2], coord[3])
    dis_31 = cal_distance(coord[3], coord[1])
    dis_13 = cal_distance(coord[0], coord[3])
    p1 = (dis_01 + dis_12 + dis_13) * 0.5
    p2 = (dis_23 + dis_31 + dis_13) * 0.5
    # 计算两个三角形的面积
    area1 = np.sqrt(p1 * (p1 - dis_01) * (p1 - dis_12) * (p1 - dis_13))
    area2 = np.sqrt(p2 * (p2 - dis_23) * (p2 - dis_31) * (p2 - dis_13))
    return area1 + area2


def rotate(angle, x, y):
    """
    基于原点的弧度旋转
    :param angle:   弧度
    :param x:       x
    :param y:       y
    :return:
    """
    rotatex = math.cos(angle) * x - math.sin(angle) * y
    rotatey = math.cos(angle) * y + math.sin(angle) * x
    return rotatex, rotatey


def xy_rorate(theta, x, y, centerx, centery):
    """
    针对中心点进行旋转
    :param theta:
    :param x:
    :param y:
    :param centerx:
    :param centery:
    :return:
    """
    r_x, r_y = rotate(theta, x - centerx, y - centery)
    return centerx + r_x, centery + r_y


def rec_rotate(x, y, width, height, theta):
    """
    传入矩形的x,y和宽度高度，弧度，转成QUAD格式
    :param x:
    :param y:
    :param width:
    :param height:
    :param theta:
    :return:
    """
    centerx = x + width / 2
    centery = y + height / 2

    x1, y1 = xy_rorate(theta, x, y, centerx, centery)
    x2, y2 = xy_rorate(theta, x + width, y, centerx, centery)

    x3, y3 = xy_rorate(theta, x + width, y + height, centerx, centery)
    x4, y4 = xy_rorate(theta, x, y + height, centerx, centery)

    return x1, y1, x2, y2, x3, y3, x4, y4


def create_json_label(filename, path_save, img_h, img_w, shapes):
    _basename = filename.split('.')[0]
    default_json = {
        "version": "3.11.0",
        "flags": {},
        "shapes": [

        ],
        "lineColor": [
            0,
            255,
            0,
            128
        ],
        "fillColor": [
            255,
            0,
            0,
            128
        ],
        "imagePath": filename,
        "imageData": None,
        "imageHeight": img_h,
        "imageWidth": img_w
    }

    # for i in range(len(points)):
    #     if len(points[i]) == 4:
    #         shape_type = "rectangle"
    #     else:
    #         shape_type = "polygon"
    #     default_shape = {
    #         "label": labels[i],
    #         "line_color": None,
    #         "fill_color": None,
    #         "points": [
    #             [
    #                 int(points[i][0]),
    #                 int(points[i][1])
    #             ],
    #             [
    #                 int(points[i][2]),
    #                 int(points[i][3])
    #             ]
    #         ],
    #         "shape_type": shape_type,
    #     }

    default_json['shapes'].extend(shapes)
    save_name = _basename + '.json'
    save_file = os.path.join(path_save, save_name)
    fp = codecs.open(save_file, 'w', encoding='utf-8')
    json.dump(default_json, fp, ensure_ascii=False)
    fp.flush()
    fp.close()


def polygon_area(points):
    """返回多边形面积

    """
    area = 0
    q = points[-1]
    for p in points:
        area += p[0] * q[1] - p[1] * q[0]
        q = p
    return area / 2


# polygon_area([[45, 272], [45, 290], [212, 296], [215, 273]])