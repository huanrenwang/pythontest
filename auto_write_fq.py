import pymysql
from datetime import *
import pandas as pd
import requests
import logging



# 要安装pymysql,chinese_calendar,pandas 使用命令pip install [xxx]

class DataBase(object):

    def __init__(self, host, port, user, pwd):
        self.db = None
        self.cursor = None
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd

    def conn(self):
        try:
            self.db = pymysql.connect(host=self.host, user=self.user, port=self.port, password=self.pwd)
        except Exception as e:
            print('连接失败')
            print(e)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.cursor.close()
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def dingding_msg(webhook_url, title, content):
    headers = {'Content-Type': 'application/json'}

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": content
        }
    }
    response = requests.post(webhook_url, json=data, headers=headers)
    return response

if __name__ == '__main__':

    # 配置日志记录
    logging.basicConfig(
        level=logging.DEBUG,  # 设置日志记录的最低级别为DEBUG（调试）级别，也可以设置为其他级别如INFO、WARNING、ERROR等
        format="%(asctime)s [%(levelname)s]: %(message)s",  # 设置日志记录的格式
        datefmt="%Y-%m-%d %H:%M:%S",  # 设置日期和时间格式
        filename="feedback.log",  # 指定日志文件名
        filemode="a"  # 设置日志文件的写入模式为追加模式（a），也可以设置为覆盖模式（w）
    )
    #现场反馈问题跟踪路径
    excel_path = 'D:\现场反馈跟踪\现场问题跟踪2023.xlsx'
    df_original = pd.read_excel(excel_path)
    host, port, user, pwd = '10.10.10.10', 3306, 'read', 'fuGtguus4yBqKF45'
    db = DataBase(host, port, user, pwd)
    feedback_data = {}
    id = []
    title = []
    product = []
    opendate = []
    current_datetime = datetime.now()
    current_date = current_datetime.date().strftime("%Y-%m-%d")
    '''SQL select fb.id,pro.name,fb.title,fb.openedDate from zt_feedback fb,zt_product pro where fb.product = pro.id and
     fb.id= 424;'''

    # 查询当日的反馈，如果有就发钉钉通知且到文件里面
    # sql = "select fb.id,pro.name,fb.title,fb.openedDate from zentaoep.zt_feedback fb,zentaoep.zt_product pro where fb.product = pro.id and fb.id= 424;"
    sql = f"select fb.id,pro.name,fb.title,fb.openedDate from zentaoep.zt_feedback fb,zentaoep.zt_product pro where fb.product = pro.id and  fb.deleted = '0' and fb.openedDate >= '{current_date}';"
    # sql = f"select fb.id,pro.name,fb.title,fb.openedDate from zentaoep.zt_feedback fb,zentaoep.zt_product pro where fb.product = pro.id and  fb.deleted = '0' and fb.openedDate >= '2023-07-10';"

    with DataBase(host, port, user, pwd) as db:
        db.conn()
        # print(db.get_list(sql))
        feedback_data_sql = db.get_list(sql)
    # print(feedback_data_sql)
    for i in feedback_data_sql:
        id.append(i["id"])
        product.append(i["name"])
        title.append(i["title"])
        opendate.append(i.get("openedDate").strftime("%m月%d日"))

    feedback_data["编号"] = id
    feedback_data["所属产品"] = product
    feedback_data["标题"] = title
    feedback_data["反馈时间"] = opendate
    # 写入到excel
    if feedback_data.get("编号"):
        print("Hello ")
        data_to_append  = feedback_data
        df_to_append = pd.DataFrame(data_to_append)
        existing_excel_file = excel_path
        df_existing = pd.read_excel(existing_excel_file)
        df_updated = pd.concat([df_existing, df_to_append], ignore_index=True)
        df_updated.to_excel(existing_excel_file, index=False)
        message_title = "现场反馈"
        message_content = ""
        lenth = len(feedback_data.get("编号"))
        for i in range(0,lenth):
            for k,v in feedback_data.items():
            # message_content += f"Hello Go\n"
                message_content += f"- {k}: {v[i]}\n"
        dingding_hooks = 'https://oapi.dingtalk.com/robot/send?access_token=331ca1761ffc8d85ec501d843cc64f9cdb34c6952a3810d3ab4f3a2be4d88799'
        response = dingding_msg(dingding_hooks, message_title, message_content)
        logging.info(f'{response.status_code}{response.text}')
        loggin.info('操作成功')
        exit(0)

    logging.info("今日无反馈")
     logging.info("今日无反馈")

