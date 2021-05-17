import csv
# import MySQLdb
# 日期列表
date_list = []
with open('DXYArea.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    flag = False
    for row in reader:
        if flag:
            a = row[11]
            date = a[5] + a[6] + '-' + a[8] + a[9]
            if date not in date_list:
                date_list.append(date)
        if not flag:
            flag = True
date_list = list(reversed(date_list))
print(date_list)
# 外国国家列表
country_list = {}
with open('DXYArea.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    flag = False
    for row in reader:
        if flag:
            a = row[2]
            if a not in country_list.keys() and a != '中国':
                country_list[a] = [0,0,0]
        if not flag:
            flag = True
print(country_list)

# conn = MySQLdb.connect(host='localhost', user='George', passwd='g1601522830', db='scraping', use_unicode=1, charset='utf8')
# cur = conn.cursor()
# today = date_list[0]
# with open('DXYArea.csv', 'r', encoding='utf8') as f:
#     reader = csv.reader(f)
#     reader = list(reader)
#     reader = list(reversed(reader))
#     day = 0
#     for row in reader[:-1]:
#         today = date_list[day]

#         time = row[11]
#         date = time[5] + time[6] + '-' + time[8] + time[9]
#         if date == today:
#             if row[2] != '中国':
#                 country_list[row[2]] = [int(row[7]), int(row[9]), int(row[10])]
#         else:
#             for i in list(country_list.keys()):

#                 cur.execute("insert into d2(month, date, country, ill, healthy, dead) values (%s, %s, %s, %s, %s, %s)", (time[5]+time[6], time[8]+time[9], i, country_list[i][0], country_list[i][1], country_list[i][2]))
#             day += 1



# for data in data_lists:
#     cur.execute("insert into d2(month, date, country, ill, healthy, dead) values (%s, %s, %s, %s, %s, %s)", (str(data[0]), str(data[1]), 'China', str(data[2]), str(data[3]), str(data[4])))

# cur.close()
# conn.commit()
# conn.close()