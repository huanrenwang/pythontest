import pymysql
from chinese_calendar import *
import datetime
from pandas import *

# 要安装pymysql,chinese_calendar,pandas 使用命令pip install [xxx]
# 特别注意,日期不支持2023以上的，如果要支持需要在元旦的时候进行更新,或者手动更新一下
# Labour Day：51 Spring Festival:春节 Tomb-sweeping Day：清明
# Dragon Boat Festival：端午 Mid-autumn Festival:中秋 National Day：国庆 New Year's Day:元旦

holidays_china = {"Dragon Boat Festival": 3, "Mid-autumn Festival": 2}


class DataBase(object):

    def __init__(self, host, port, user, pwd):
        self.db = None
        self.cursor = None
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.name = name

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


if __name__ == '__main__':
    host, port, user, pwd = '10.10.10.10', 3306, 'read', 'fuGtguus4yBqKF45'
    db = DataBase(host, port, user, pwd)
    # sql = "select * from zentaoep.zt_bug where id = '13136';"
    # 查询对应的项目对应的分支的缺陷
    # sql = "select id, openedDate, resolvedDate from zentaoep.zt_bug where project = 163 and branch = 3 and openedDate >= '2023-03-01 00:00:00'"
    # 查对应产品的缺陷算解决周期，时间切记要修改成自己的时间
    sql_resoved = ''' select pr.name, bug.id, bug.openedDate, bug.resolvedDate 
                  from zentaoep.zt_product pr, zentaoep.zt_bug bug 
    where pr.id = bug.product and pr.name in ('下一代网络靶场','拟态蜜网', '主动防御网关', 'BAS安全验证系统')
    and bug.openedDate >= '2023-03-01 00:00:00' and bug.deleted <> '1' and bug.status = 'resolved' '''

    # 查对应产品的缺陷算关闭周期，时间切记要修改成自己的时间
    sql_closed = ''' select pr.name, bug.id, bug.openedDate, bug.resolvedDate, bug.closedDate 
    from zentaoep.zt_product pr, zentaoep.zt_bug bug where pr.id = bug.product and pr.name in ('下一代网络靶场','拟态蜜网', '主动防御网关', 'BAS安全验证系统')
    and bug.openedDate >= '2023-03-01 00:00:00' and bug.deleted <> '1' and bug.status = 'closed' '''

    with DataBase(host, port, user, pwd) as db:
        db.conn()
        # print(db.get_list(sql))
        bug_data = db.get_list(sql_resoved)
        bug_close = db.get_list(sql_closed)
    # print(bug_data)
    days_bug = []
    close_bug = []
    for bug in bug_data:
        day = bug.get('openedDate') + datetime.timedelta(days=1)
        resolved_day = bug.get('resolvedDate')
        # 用来比较节假日是否修复了缺陷
        if is_holiday(day):
            holiday_detail = get_holiday_detail(day)
            # 国家法定节假日的
            if holiday_detail and holidays_china.get(holiday_detail):
                tmp_holiday = bug.get('openedDate') + datetime.timedelta(days=(holidays_china.get(holiday_detail)))
                if resolved_day > tmp_holiday:
                    resolved_date = resolved_day - datetime.timedelta(
                        days=(holidays_china.get(holiday_detail))) - bug.get('openedDate')
                else:
                    resolved_date = resolved_day - bug.get('openedDate')

            # 正常周末
            else:
                tmp_holiday = bug.get('openedDate') + datetime.timedelta(days=2)
                if resolved_day > tmp_holiday:
                    # resolved_date = resolved_day - datetime.timedelta(days=2) - bug.get('openedDate')
                    resolved_date = round(
                        (resolved_day - datetime.timedelta(days=2) - bug.get('openedDate')).days * 24) + round(
                        (resolved_day - datetime.timedelta(days=2) - bug.get('openedDate')).seconds / 3600, 2)
                else:
                    # resolved_date = resolved_day - bug.get('openedDate')
                    resolved_date = round(
                        (resolved_day - bug.get('openedDate')).days * 24) + round(
                        (resolved_day - bug.get('openedDate')).seconds / 3600, 2)
            bug.setdefault("resolve_cycle", resolved_date)
            days_bug.append(bug)
        # 非节假日
        else:
            resolved_date = round((resolved_day - bug.get('openedDate')).days * 24) + round(
                (resolved_day - bug.get('openedDate')).seconds / 3600, 2)
            bug.setdefault("resolve_cycle", resolved_date)
            days_bug.append(bug)

    # 开始计算关闭周期的数据
    for bg in bug_close:
        openday = bg.get('openedDate')
        closeday = bg.get('resolvedDate')
        close_cycle = (closeday - openday).days * 24 + round((closeday - openday).seconds / 3600, 2)
        bg.setdefault("close_cycle", close_cycle)
        close_bug.append(bg)

    df = DataFrame(days_bug)
    df.to_excel('resolve.xlsx')
    df = DataFrame(close_bug)
    df.to_excel('close.xlsx')
