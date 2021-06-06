import argparse
import base64
import json
import os
import os.path as osp

import imgviz
import PIL.Image

from labelme.logger import logger
from labelme import utils

from threading import Thread


def save_file(img, res_path, lbl, lbl_viz, label_names):
    PIL.Image.fromarray(img).save(osp.join(res_path, "img.png"))
    utils.lblsave(osp.join(res_path, "label.png"), lbl)
    PIL.Image.fromarray(lbl_viz).save(osp.join(res_path, "label_viz.png"))

    with open(osp.join(res_path, "label_names.txt"), "w") as f:
        for lbl_name in label_names:
            f.write(lbl_name + "\n")

    logger.info("Saved to: {}".format(res_path))


def main():
    thread_pool = []

    logger.warning(
        "This script is aimed to demonstrate how to convert the "
        "JSON file to a single image dataset."
    )
    logger.warning(
        "It won't handle multiple JSON files to generate a "
        "real-use dataset."
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    parser.add_argument("-o", "--out", default=None)
    args = parser.parse_args()

    json_file = args.json_file

    if args.out is None:
        out_dir = osp.basename(json_file).replace(".", "_")
        out_dir = osp.join(osp.dirname(json_file), out_dir)
    else:
        out_dir = args.out
    if not osp.exists(out_dir):
        os.mkdir(out_dir)

    # data = json.load(open(json_file))

    for j in os.listdir(json_file):
        if j.endswith("json"):
            json_path = f"{json_file}/{j}"
            res_path = f"{out_dir}/{j[:-5]}"
            if not os.path.exists(res_path):
                os.mkdir(res_path)
            data = json.load(open(json_path))
            imageData = data.get("imageData")

            if not imageData:
                imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
                with open(imagePath, "rb") as f:
                    imageData = f.read()
                    imageData = base64.b64encode(imageData).decode("utf-8")
            img = utils.img_b64_to_arr(imageData)

            label_name_to_value = {"_background_": 0}
            for shape in sorted(data["shapes"], key=lambda x: x["label"]):
                label_name = shape["label"]
                if label_name in label_name_to_value:
                    label_value = label_name_to_value[label_name]
                else:
                    label_value = len(label_name_to_value)
                    label_name_to_value[label_name] = label_value
            lbl, _ = utils.shapes_to_label(
                img.shape, data["shapes"], label_name_to_value
            )

            label_names = [None] * (max(label_name_to_value.values()) + 1)
            for name, value in label_name_to_value.items():
                label_names[value] = name

            lbl_viz = imgviz.label2rgb(
                label=lbl, img=imgviz.asgray(img), label_names=label_names, loc="rb"
            )
            # 采用多线程保存文件
            t = Thread(target=save_file, args=(img, res_path, lbl, lbl_viz, label_names))
            t.start()
            thread_pool.append(t)

    for t in thread_pool:
        t.join()

            # PIL.Image.fromarray(img).save(osp.join(res_path, "img.png"))
            # utils.lblsave(osp.join(res_path, "label.png"), lbl)
            # PIL.Image.fromarray(lbl_viz).save(osp.join(res_path, "label_viz.png"))
            #
            # with open(osp.join(res_path, "label_names.txt"), "w") as f:
            #     for lbl_name in label_names:
            #         f.write(lbl_name + "\n")
            #
            # logger.info("Saved to: {}".format(res_path))


if __name__ == "__main__":
    main()
