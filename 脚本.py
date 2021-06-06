import json
import os
import shutil
import numpy as np
import cv2
from tqdm import tqdm

# json路径
PATH = r"imgs"
# 切图根路径
DIR_PATH = r"simple_defect"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _get_box(points):
    min_x = min_y = np.inf
    max_x = max_y = 0
    for x, y in points:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return [min_x, min_y, max_x - min_x, max_y - min_y]


for filename in tqdm(os.listdir(PATH)):
    filepath = os.path.join(PATH, filename)
    # 存储提取json出来的图片路径
    res_path = "res"
    # 找到json
    if "json" in filename:
        # 读取json内容
        with open(filepath, "r", encoding="utf-8") as f:
            content = json.load(f)["shapes"]
        # json路径
        print(filepath)
        # 指定准备裁切的小缺陷图属于哪个annotation: new_filepath
        newfilepathName = filename[:-5]
        new_filepath = f"{DIR_PATH}/{newfilepathName}"
        if not os.path.exists(new_filepath):
            os.mkdir(new_filepath)
        # img_path = os.path.join(PATH, f"{os.path.splitext(filename)[0]}.jpg")
        img_path = filepath.replace("json", "jpg")
        label_viz_path = res_path + "/" + newfilepathName + "/" + "label_viz.png"
        print(f"label_viz_path: {label_viz_path}")
        # 		print(img_path)
        img = cv2.imread(img_path)  # 原图
        label_viz = cv2.imread(label_viz_path)  # 读取label_viz.png
        # print(label_viz.shape)
        # 		print("img:",img)
        # 获取每种缺陷类型数据
        count = 1
        for detect_data in content:
            label = detect_data["label"]
            print(label)
            points = detect_data["points"]
            point_l = np.array(points, dtype=int)
            area = cv2.contourArea(point_l)  # 单个缺陷面积

            print(f"{label} area: {area}")

            # 坐标转换
            print("points:", points)
            x, y, w, h = _get_box(points)
            print(x, y, w, h, count)
            # 从原图中切出小图
            # img_split = img[(int(y) - 3):(int(y) + int(h) + 3), (int(x) - 3):(int(x) + int(w) + 3), :]
            # img_split = img[int(y) - 3:int(y) + int(h) + 3, int(x) - 3:int(x) + int(w) + 3, :]  # 目标小图
            # 从提前分离出来的label_viz.png中切出小图
            img_split = label_viz[int(y) - 3:int(y) + int(h) + 6, int(x) - 3:int(x) + int(w) + 6, :]  # 目标小图
            # 创建存图目录
            try:
                # 生成与之对应的json同名的目录
                img_split_dir = os.path.join(new_filepath, label)  # 此处可以按照需求改成只生成以缺陷名称为目录
                os.mkdir(img_split_dir)
            except FileExistsError:
                pass
            # 保存小图
            # 小图名
            img_split_name = f"{os.path.splitext(filename)[0]}_{count}.jpg"
            count += 1
            img_split_path = os.path.join(img_split_dir, img_split_name)
            # 存图
            if int(y) - 3 < 0 or int(x) - 3 < 0 or img_split.shape[0] == 0 or img_split.shape[1] == 1:
                print("img_split:", img_split.shape, filepath)
            # 			print("img_split:",img_split.shape)
            cv2.imwrite(img_split_path, img_split)
        # # # 如果出现其他缺陷类型，提取出json
        # detect_type = ["dent", "scratch", "contamination", "fiber",
        #                "cloud", "ink-break", "pollen", "wavelet"]
        # if label not in detect_type:
        #     try:
        #         os.mkdir(os.path.join(DIR_PATH, "exist_error"))
        #     except FileExistsError:
        #         pass
        #     # 复制json
        #     new_path = os.path.join(DIR_PATH, "exist_error", os.path.split(filepath)[1])
        #     shutil.copy(filepath, new_path)
