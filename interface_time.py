import copy
import math
import os
import re
import pandas as pd

if __name__ == '__main__':

    pattern = r'url=(.*?)upstream_addr=(.*?)request_time=(.*?)$'
    interface_list = []
    interface_list_result = []
    # 读取文件并且过滤时间小于500毫秒的数据
    with open('./api.info', 'r+') as f:
        for line in f.readlines():
            face_dict = {}
            if "/page/" not in line and "/api/mp/file" not in line and "/ws/" not in line:
                line = re.search(pattern, line)
                if line:
                    face_dict[line.group(1).strip()] = float(line.group(3))
                    if face_dict[line.group(1).strip()] > 0.5:
                        interface_list.append(face_dict)
    # 去重相差不大的接口数据
    for i in range(0, len(interface_list)):
        if interface_list[i]:
            for k1, v1 in interface_list[i].items():
                for j in range(i + 1, len(interface_list)):
                    if i + 1 == len(interface_list):
                        break
                    if interface_list[j]:
                        for k2, v2 in interface_list[j].items():
                            if k2 == k1 and math.fabs(v2 - v1) < 0.5:
                                interface_list[j] = None
    for i in interface_list:
        if isinstance(i, dict):
            interface_dict = {}
            for k,v in i.items():
                interface_dict['interface_name'] = k
                interface_dict['time'] = v
            interface_list_result.append(interface_dict)
    print(interface_list_result)
    excel_path = "./interface.xlsx"
    df = pd.DataFrame(interface_list_result)
    writer = pd.ExcelWriter(excel_path)
    df.to_excel(writer, index=False)
    writer._save()
    print("Hello World")
    print(i)





