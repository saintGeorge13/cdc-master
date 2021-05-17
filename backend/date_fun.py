# -*- coding: UTF-8 -*- 
import datetime
# 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
def getdate(date, beforeOfDay):
    date_ = date.split('-')
    date_ = [int(i) for i in date_]
    # print(date_)
    today = datetime.date(date_[0], date_[1], date_[2])
    # print(today)
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    pre_date = (today + offset).strftime('%Y-%m-%d')
    return pre_date
if __name__ == "__main__":
    print(getdate("2020-02-01", 1))