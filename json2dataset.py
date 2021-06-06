# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name:         json2dataset
# Description:  Bug,不存在的！
# Author:       xuxianghang
# Date:         2021/6/5 17:56
# IDE:          PyCharm
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import os
from threading import Thread
import time


def test_json2dataset(json_path, res_path):
    os.system(f"labelme_json_to_dataset {json_path} -o {res_path}")


if __name__ == "__main__":
    thread_pool = []
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    json_path = f"{BASE_DIR}\\imgs"  # include json file.
    res_path = f"{BASE_DIR}\\res"

    time1 = time.time()
    # t = Thread(target=test_json2dataset, args=(json_path, res_path))
    # t.start()
    # thread_pool.append(t)
    # for t in thread_pool:
    #     t.join()
    test_json2dataset(json_path, res_path)
    time2 = time.time()
    use_time = time2 - time1
    print(use_time)  # use thread: 11.310834646224976, no thread: 11.374838829040527
