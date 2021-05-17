import csv
import pymysql
import pypinyin

# 不带声调的(style=pypinyin.NORMAL)
def hp(word):
    if word == '陕西':
        return 'shaanxi'
    else:
        s = ''
        for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            s += ''.join(i)
        return s

# 日期列表
date_list = []
conn = pymysql.connect(host='118.31.41.159', user='root', passwd='12Li2969/', db='data', use_unicode=1, charset='utf8')
cur = conn.cursor()
cur.execute('select date from data where country = "country" and province = "province" and city = "city"')
results = cur.fetchall()
for i in range(len(results)):
    date = ''.join(str(results[i][0]))
    date_list.append(date[-5:])
date_list = sorted(date_list)

# with open('DXYArea.csv', 'r', encoding='utf8') as f:
#     reader = csv.reader(f)
#     flag = False
#     for row in reader:
#         if flag:
#             a = row[11]
#             date = a[5] + a[6] + '-' + a[8] + a[9]
#             if date not in date_list:
#                 date_list.append(date)
#         if not flag:
#             flag = True
# date_list = list(reversed(date_list))
# print(date_list)

# 外国国家列表
# country_list = {}
# with open('DXYArea.csv', 'r', encoding='utf8') as f:
#     reader = csv.reader(f)
#     flag = False
#     for row in reader:
#         if flag:
#             a = row[3]# 这一列是国家的英文
#             if a not in country_list.keys() and a != 'China':
#                 country_list[a] = [0, 0, 0]
#         if not flag:
#             flag = True
# # print(country_list.keys())


# 省市列表
# 省有哪些市
# province_list = {}
# with open('DXYArea.csv', 'r', encoding='utf8') as f:
#     reader = csv.reader(f)
#     flag = False
#     for row in reader:
#         if flag:
#             if row[3] == 'China':
#                 if row[5] not in province_list.keys() and row[5] != 'China':
#                     province_list[row[5]] = []
#                 if row[13] != '' and row[12] not in province_list[row[5]]:
#                     province_list[row[5]].append(row[12])
#         if not flag:
#             flag = True

# print(province_list)
# city_list = {}
# with open('DXYArea.csv', 'r', encoding='utf8') as f:
#     reader = csv.reader(f)
#     flag = False
#     for row in reader:
#         if flag:
#             if row[3] == 'China':
#                 if row[13] != '' and row[12] not in city_list.keys():
#                     city_list[row[12]] = [0, 0, 0]
#         if not flag:
#             flag = True

# print(city_list)

# 台湾香港澳门
# Hong_Kong = [0, 0, 0]
# Taiwan = [0, 0, 0]
# Macau = [0, 0, 0]

# # 插入数据库
# conn = pymysql.connect(host='118.31.41.159', user='root', passwd='12Li2969/', db='data', use_unicode=1, charset='utf8')
# cur = conn.cursor()
# today = date_list[0]
# # sql = """CREATE TABLE data (
# #          date Date NOT NULL,
# #          country varchar(100) not null,
# #          province varchar(100),
# #          city varchar(100),
# #          confirmed int not null,
# #          cured int not null,
# #          death int not null)"""
# #
# # cur.execute(sql)
# with open('DXYArea.csv', 'r', encoding='utf8') as f:
#     reader = csv.reader(f)
#     reader = list(reader)
#     reader = list(reversed(reader))
#     day = 0
#     for row in reader[:]:
#         today = date_list[day]
#         time = row[11]
#         date = time[5] + time[6] + '-' + time[8] + time[9]
#         if date == today:
#             if row[3] != 'China':
#                 country_list[row[3]] = [int(row[7]), int(row[9]), int(row[10])]
#             elif row[3] == 'China' and row[13] != '' and row[12] != '':
#                 city_list[row[12]] = [int(row[15]), int(row[17]), int(row[18])]
#             if row[3] == 'China' and row[5] == 'Hong Kong':
#                 Hong_Kong = [int(row[7]), int(row[9]), int(row[10])]
#             if row[3] == 'China' and row[5] == 'Taiwan':
#                 Taiwan = [int(row[7]), int(row[9]), int(row[10])]
#             if row[3] == 'China' and row[5] == 'Macau':
#                 Macau = [int(row[7]), int(row[9]), int(row[10])]
#
#         elif date != today:
#             w = 1
#             # 全世界
#             # print(w)
#             # confirmed = 0
#             # cured = 0
#             # death = 0
#             # for i in list(country_list.keys()):
#             #     confirmed += country_list[i][0]
#             #     cured += country_list[i][1]
#             #     death += country_list[i][2]
#             # for city in city_list:
#             #     confirmed += city_list[city][0]
#             #     cured += city_list[city][1]
#             #     death += city_list[city][2]
#             # cur.execute(
#             #     "insert into data(date, country, province, city, confirmed, cured, death) values (%s, %s, %s, %s, %s, %s, %s)",
#             #     ('2020' + '-' + today, 'country', 'province', 'city', confirmed, cured, death))
#             # 外国
#             # for i in list(country_list.keys()):
#             #     cur.execute("insert into data(date, country, confirmed, cured, death) values (%s, %s, %s, %s, %s)", ('2020'+'-'+today, i, country_list[i][0], country_list[i][1], country_list[i][2]))
#             # 中国各市
#             # for i in list(city_list.keys()):
#             #     for j in province_list.keys():
#             #         if i in province_list[j]:
#             #             province = j
#             #
#             #     cur.execute("insert into data(date, country, province, city, confirmed, cured, death) values (%s, %s, %s, %s, %s, %s, %s)", ('2020'+'-'+today, 'China', hp(province), hp(i), city_list[i][0], city_list[i][1], city_list[i][2]))
#             #     print(w)
#             #     w += 1
#             #
#             # # 各省的
#             # for province in province_list.keys():
#             #     confirmed = 0
#             #     cured = 0
#             #     death = 0
#             #     for city in province_list[province]:
#             #         if hp(city) == 'daimingquediqu' or hp(city) == 'People from other cities':
#             #             continue
#             #         confirmed += city_list[city][0]
#             #         cured += city_list[city][1]
#             #         death += city_list[city][2]
#             #     cur.execute(
#             #         "insert into data(date, country, province, city, confirmed, cured, death) values (%s, %s, %s, %s, %s, %s, %s)",
#             #         ('2020' + '-' + today, 'China', hp(province), 'city', confirmed, cured, death))
#             #
#             # # 中国
#             # print(w)
#             # confirmed = 0
#             # cured = 0
#             # death = 0
#             # for city in city_list:
#             #     confirmed += city_list[city][0]
#             #     cured += city_list[city][1]
#             #     death += city_list[city][2]
#             # cur.execute(
#             #     "insert into data(date, country, province, city, confirmed, cured, death) values (%s, %s, %s, %s, %s, %s, %s)",
#             #     ('2020' + '-' + today, 'China', 'province', 'city', confirmed, cured, death))
#             # # 台湾香港澳门
#             # cur.execute("insert into data(date, country, province, confirmed, cured, death) values(%s, %s, %s, %s, %s, %s)", ('2020' + '-' + today, 'China', 'Hong Kong', Hong_Kong[0], Hong_Kong[1],Hong_Kong[2]))
#             # cur.execute("insert into data(date, country, province, confirmed, cured, death) values(%s, %s, %s, %s, %s, %s)", ('2020' + '-' + today, 'China', 'Taiwan', Taiwan[0], Taiwan[1], Taiwan[2]))
#             # cur.execute("insert into data(date, country, province, confirmed, cured, death) values(%s, %s, %s, %s, %s, %s)", ('2020' + '-' + today, 'China', 'Macau', Macau[0], Macau[1], Macau[2]))
#             day += 1
#
# cur.close()
# conn.commit()
# conn.close()
# #
# # # 用户名密码
# # conn = pymysql.connect(host='118.31.41.159', user='root', passwd='12Li2969/', db='data', use_unicode=1, charset='utf8')
# # cur = conn.cursor()
# # sql = """CREATE TABLE username(
# #     username varchar(100) not null,
# #     password varchar(100) not null,
# #     primary key(username)
# #     )"""
# # cur.execute(sql)
# # cur.close()
# # conn.commit()
# # conn.close()