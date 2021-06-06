# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         test
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/6/5 15:10
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import os
import subprocess
from threading import Thread

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
imgs_path = f"{BASE_DIR}\\imgs"  # include json file.
res_path = f"{BASE_DIR}\\res"


def json2dataset(json_path, per_res_dirname_path):
    # subp = subprocess.Popen(f"labelme_json_to_dataset {json_path} -o {per_res_dirname_path}",
    #                  shell=True, stdout=subprocess.PIPE)
    # if subp.poll() == 0:
    #     print(subp.communicate()[1])
    # else:
    #     print("失败")
    os.system(f"labelme_json_to_dataset {json_path} -o {per_res_dirname_path}")


def mkdir_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


thread_pool = []
for i in os.listdir(imgs_path):
    x = 1
    if i.endswith("json"):
        json_path = f"{imgs_path}\\{i}"
        per_res_dirname = i[:-5]
        print(per_res_dirname)
        per_res_dirname_path = f"{res_path}\\{per_res_dirname}"
        if not os.path.exists(per_res_dirname_path):
            os.mkdir(per_res_dirname_path)
        if os.path.exists(per_res_dirname_path):
            print(f"*********** 开始转化第{x}个json----------")
            t = Thread(target=json2dataset, args=(json_path, per_res_dirname_path))
            t.start()
            thread_pool.append(t)

        print(f"*********** 转化第{x}个json结束----------")
    x += 1

for t in thread_pool:
    t.join()
