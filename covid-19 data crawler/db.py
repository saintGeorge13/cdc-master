"""
@ProjectName: DXY-2019-nCov-Crawler
@FileName: db.py
@Author: Jiabao Lin
@Date: 2020/1/21
"""
import pymysql
import datetime

class DB:
    def __init__(self):
        self.db = pymysql.connect(host="localhost", user="root", password="12Li2969/", database="data", charset="utf8")
        # self.db = pymysql.connect(host="localhost", user="root", password="12li2969", database="covid_data", charset="utf8")# home db test
        

    def insert(self, date, country, province, city, confirmed, cured, death):
        cursor = self.db.cursor()
        date = str(datetime.date.today())
        if province == None:
            province = "NUll"
        if city == None:
            city = "NULL"
        
        sql = "INSERT INTO data (date, country, province, city, confirmed, cured, death) VALUES('%s', '%s', '%s', '%s', %s, %s, %s);"%(date, country, province, city, str(confirmed), str(cured), str(death))
        # sql = "INSERT INTO covid_data (date, country, province, city, confirmed, cured, death) VALUES('%s', '%s', '%s', '%s', %s, %s, %s);"%(date, country, province, city, str(confirmed), str(cured), str(death))
        # print(sql)
        cursor.execute(sql)
        cursor.close()
        self.db.commit()

if __name__ == "__main__":
    # test = DB()
    pass
    