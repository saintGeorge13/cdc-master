import pymysql
import date_fun
import createdb
import csv

class database:
    def __init__(self):
        self.db = pymysql.connect(host='118.31.41.159', user='root', passwd='12Li2969/', db='data', use_unicode=1, charset='utf8')
        self.cursor = self.db.cursor()
        self.fields = ["date", "country", "province", "city", "confirmed", "cured", "death"]
        self.fields2 = ["date", "country", "confirmed", "cured", "death"]

    def get_data_accumulated(self, date, country, province='', city=''):
        """
            return the accumulated data till date time
            date: "YYYY-MM-DD"
            country: "中文"
            province: "中文"
            city: "中文"
        """
        if province != '' and city != '':
            sql = 'SELECT * from data where date = "{}" AND country = "{}" AND province = "{}" AND city = "{}"'.format(date, country, province, city)
        elif province == '' or city == '':
            sql = "SELECT date, country, confirmed, cured, death from data where date = '{}' AND country = '{}'".format(date, country)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            ans = {}
            for i in range(len(results[0])):
                if province != '' and city != '':
                    if i == 0:
                        ans[self.fields[i]] = str(results[0][i])
                    else:
                        ans[self.fields[i]] = results[0][i]
                elif province == '' or city == '':
                    if i == 0:
                        ans[self.fields2[i]] = str(results[0][i])
                    else:
                        ans[self.fields2[i]] = results[0][i]
            # print(ans)
            return ans
        except Exception as e:
            print(e)
            print("Error: unable to fetch data")

    def get_data_date(self, date, country, province, city):
        """
            return the accumulated data till date time
            date: "YYYY-MM-DD"
            country: "中文"
            province: "中文"
            city: "中文"
        """
        pre_day = date_fun.getdate(date, 1)
        pre_data = self.get_data_accumulated(pre_day, country, province, city)
        date_data = self.get_data_accumulated(date, country, province, city)
        for i in range(len(pre_data)):
            if i < 4:
                continue
            else:
                date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
        print(date_data)
        return date_data

    def get_country_list(self, date):
        self.cursor.execute('select country from data where date = "{}"'.format(date))
        results = self.cursor.fetchall()
        country_list = []
        for i in range(len(results)):
            country = ''.join(results[i])
            if country != 'China':
                country_list.append(country)
        return country_list

    def get_province_list(self, date):
        self.cursor.execute('select province, city from data where date="{}" and country="{}"'.format(date, 'China'))
        results = self.cursor.fetchall()
        # print(results)
        province_list = {}
        for item in results:
            if item[0] != "NULL" and item[1] != "NULL":
                if item[0].lower() not in province_list.keys():
                    province_list[item[0].lower()] = []
                if item[1] not in province_list[item[0].lower()]:
                    province_list[item[0].lower()].append(item[1])
        return province_list

    def barchart(self, Type, date, country='', province=''):
        # 如果country='', province必须='',外国;如果country!='' province='',中国各省;如果country!='' province='',该省的各市
        # 外国
        if country == '':
            country_list = self.get_country_list(date) # 所有外国国家
            # 格式 {'USA': {'date': '2020-4-1', 'country': 'USA', 'confirmed': '1', 'cured': '1', 'death': '2'}}
            all_country_date_data = {}
            if Type == 'accumulated':
                for country in country_list:
                    date_data = self.get_data_accumulated(date, country)
                    all_country_date_data[country] = date_data
                all_country_date_data['China'] = self.get_data_accumulated(date, 'China', 'province', 'city')
                del all_country_date_data['China']['province']
                del all_country_date_data['China']['city']
                return all_country_date_data
            if Type == 'someday':
                for country in country_list:
                    pre_day = date_fun.getdate(date, 1)
                    date_data = self.get_data_accumulated(date, country)
                    if pre_day != '2020-01-21':
                        pre_data = self.get_data_accumulated(pre_day, country)
                        for i in range(len(pre_data)):
                            if i < 2:
                                continue
                            else:
                                date_data[self.fields2[i]] = date_data[self.fields2[i]] - pre_data[self.fields2[i]]
                    all_country_date_data[country] = date_data
                date_data = self.get_data_accumulated(date, 'China', 'province', 'city')
                pre_day = date_fun.getdate(date, 1)
                if pre_day != '2020-01-21':
                    pre_data = self.get_data_accumulated(pre_day, 'China', 'province', 'city')
                    for i in range(len(pre_data)):
                        if i < 4:
                            continue
                        else:
                            date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                all_country_date_data['China'] = date_data
                del all_country_date_data['China']['province']
                del all_country_date_data['China']['city']
                return all_country_date_data
        # 中国
        # 全国各省
        elif country != '':
            if province == '':
                # 格式 {'guangdong': {'date': '2020-4-1', 'country': 'China', 'province':'gd', confirmed': '1', 'cured': '1', 'death': '2'}}
                all_province_date_data = {}
                province_list = self.get_province_list(date)

                if Type == 'accumulated':
                    for province in province_list.keys():
                        # province_date_data = {'date': date, 'country': 'China', 'province': province, 'confirmed': 0, 'cured': 0, 'death': 0}
                        # for city in province_list[province]:
                        #     # 这些数据要删除
                        #     if city is None or createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities' :
                        #         continue
                        #     date_data = self.get_data_accumulated(date, country, province, createdb.hp(city))
                        #     province_date_data['confirmed'] += date_data['confirmed']
                        #     province_date_data['cured'] += date_data['cured']
                        #     province_date_data['death'] += date_data['death']
                        province_date_data = {'date': date, 'country': 'China', 'province': province, 'confirmed': 0, 'cured': 0, 'death': 0}
                        date_data = self.get_data_accumulated(date, country, createdb.hp(province), 'city')

                        province_date_data['confirmed'] += date_data['confirmed']
                        province_date_data['cured'] += date_data['cured']
                        province_date_data['death'] += date_data['death']
                        all_province_date_data[province] = province_date_data
                    return all_province_date_data
                if Type == 'someday':
                    pre_day = date_fun.getdate(date, 1)
                    for province in province_list.keys():
                        # province_date_data = {'date': date, 'country': 'China', 'province': province, 'confirmed': 0, 'cured': 0, 'death': 0}
                        # for city in province_list[province]:
                        #     # 这些数据要删除
                        #     if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                        #         continue
                        #     date_data = self.get_data_accumulated(date, country, province, createdb.hp(city))
                        #     if pre_day != '2020-01-21':
                        #         pre_data = self.get_data_accumulated(pre_day, country, province, createdb.hp(city))
                        #         for i in range(len(pre_data)):
                        #             if i < 4:
                        #                 continue
                        #             else:
                        #                 date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                        #     province_date_data['confirmed'] += date_data['confirmed']
                        #     province_date_data['cured'] += date_data['cured']
                        #     province_date_data['death'] += date_data['death']
                        date_data = self.get_data_accumulated(date, country, createdb.hp(province), 'city')
                        province_date_data = {'date': date, 'country': 'China', 'province': province, 'confirmed': 0, 'cured': 0, 'death': 0}
                        if pre_day != '2020-01-21':
                            pre_data = self.get_data_accumulated(pre_day, country, createdb.hp(province), 'city')
                            for i in range(len(pre_data)):
                                if i < 4:
                                    continue
                                else:
                                    date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                        province_date_data['confirmed'] += date_data['confirmed']
                        province_date_data['cured'] += date_data['cured']
                        province_date_data['death'] += date_data['death']
                        all_province_date_data[province] = province_date_data
                    return all_province_date_data
            # 该省各市
            if province != '':
                # 格式 {'guangzhou': {'date': '2020-04-01', 'country': 'China', 'province':'gd', 'city': 'gz', confirmed': '1', 'cured': '1', 'death': '2'}}
                all_city_date_data = {}
                province_list = self.get_province_list(date)
                if Type == 'accumulated':
                    for city in province_list[createdb.hp(province)]:
                        # 这些数据要删除
                        if createdb.hp(city) == 'city' or createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                            continue
                        date_data = self.get_data_accumulated(date, country, createdb.hp(province), createdb.hp(city))
                        all_city_date_data[createdb.hp(city)] = date_data
                    return all_city_date_data
                if Type == 'someday':
                    pre_day = date_fun.getdate(date, 1)
                    for city in province_list[createdb.hp(province)]:
                        # 这些数据要删除
                        if createdb.hp(city) == 'city' or createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                            continue
                        date_data = self.get_data_accumulated(date, country, createdb.hp(province), createdb.hp(city))
                        if pre_day != '2020-01-21':
                            pre_data = self.get_data_accumulated(pre_day, country, createdb.hp(province), createdb.hp(city))
                            for i in range(len(pre_data)):
                                if i < 4:
                                    continue
                                else:
                                    date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                        all_city_date_data[createdb.hp(city)] = date_data
                    return all_city_date_data

    def linechart(self, Type, Date, country='', province='', city=''):
        if city != '' and province != '':
            city_date_data = {}
            if Type == 'accumulated':
                for date in createdb.date_list:
                    if '2020-' + date == Date:
                        break
                    date_data = self.get_data_accumulated('2020-' + date, country, createdb.hp(province), createdb.hp(city))
                    city_date_data['2020-' + date] = date_data
                return city_date_data
            if Type == 'someday':
                for date in createdb.date_list:
                    if '2020-' + date == Date:
                        break
                    pre_day = date_fun.getdate('2020-' + date, 1)
                    date_data = self.get_data_accumulated('2020-' + date, country, createdb.hp(province), createdb.hp(city))
                    if pre_day != '2020-01-21':
                        pre_data = self.get_data_accumulated(pre_day, country, createdb.hp(province), createdb.hp(city))
                        for i in range(len(pre_data)):
                            if i < 4:
                                continue
                            else:
                                date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                    city_date_data['2020-' + date] = date_data
                return city_date_data
        if city == '' and province != '':
            province_list = self.get_province_list(Date)
            all_province_date_data = {}
            if Type == 'accumulated':
                for date in createdb.date_list:
                    if '2020-' + date == Date:
                        break
                    date_data = self.get_data_accumulated('2020-'+date, country, createdb.hp(province), 'city')
                    province_date_data = {'date': '2020-'+date, 'country': 'China', 'province': createdb.hp(province), 'confirmed': 0,
                                          'cured': 0, 'death': 0}
                    province_date_data['confirmed'] += date_data['confirmed']
                    province_date_data['cured'] += date_data['cured']
                    province_date_data['death'] += date_data['death']
                    # province_date_data = {'date': '2020-'+date, 'country': 'China', 'province': province, 'confirmed': 0,
                    #                       'cured': 0, 'death': 0}
                    # province_list = self.get_province_list(Date)
                    # for city in province_list[province]:
                    #     # 这些数据要删除
                    #     if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                    #         continue
                    #     date_data = self.get_data_accumulated('2020-'+date, country, province, createdb.hp(city))
                    #     province_date_data['confirmed'] += date_data['confirmed']
                    #     province_date_data['cured'] += date_data['cured']
                    #     province_date_data['death'] += date_data['death']
                    all_province_date_data['2020-' + date] = province_date_data
                return all_province_date_data
            if Type == 'someday':
                for date in createdb.date_list:
                    if '2020-' + date == Date:
                        break
                    date_data = self.get_data_accumulated('2020-'+date, country, createdb.hp(province), 'city')
                    province_date_data = {'date': '2020-' + date, 'country': 'China', 'province': createdb.hp(province),
                                          'confirmed': 0, 'cured': 0, 'death': 0}
                    pre_day = date_fun.getdate('2020-' + date, 1)
                    if pre_day != '2020-01-21':
                        pre_data = self.get_data_accumulated(pre_day, country, createdb.hp(province), 'city')
                        for i in range(len(pre_data)):
                            if i < 4:
                                continue
                            else:
                                date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                    province_date_data['confirmed'] += date_data['confirmed']
                    province_date_data['cured'] += date_data['cured']
                    province_date_data['death'] += date_data['death']
                    all_province_date_data['2020-' + date] = province_date_data
                    # province_date_data = {'date': '2020-'+date, 'country': 'China', 'province': province, 'confirmed': 0,
                    #                       'cured': 0, 'death': 0}
                    # pre_day = date_fun.getdate('2020-'+date, 1)
                    # province_list = self.get_province_list(Date)
                    # for city in province_list[province]:
                    #     # 这些数据要删除
                    #     if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                    #         continue
                    #     date_data = self.get_data_accumulated('2020-'+date, country, province, createdb.hp(city))
                    #     if pre_day != '2020-01-21':
                    #         pre_data = self.get_data_accumulated(pre_day, country, province, createdb.hp(city))
                    #         for i in range(len(pre_data)):
                    #             if i < 4:
                    #                 continue
                    #             else:
                    #                 date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                    #     province_date_data['confirmed'] += date_data['confirmed']
                    #     province_date_data['cured'] += date_data['cured']
                    #     province_date_data['death'] += date_data['death']
                    # all_province_date_data['2020-' + date] = province_date_data
                return all_province_date_data
        if city == '' and province == '' and country.lower() != 'china' and country != '':
            all_country_date_data = {}
            if Type == 'accumulated':
                for date in createdb.date_list:
                    if '2020-' + date == Date:
                        break
                    date_data = self.get_data_accumulated('2020-'+date, country)
                    all_country_date_data['2020-'+date] = date_data
                return all_country_date_data
            if Type == 'someday':
                for date in createdb.date_list:
                    if '2020-' + date == Date:
                        break
                    pre_day = date_fun.getdate('2020-'+date, 1)
                    date_data = self.get_data_accumulated('2020-'+date, country)
                    if pre_day != '2020-01-21':
                        pre_data = self.get_data_accumulated(pre_day, country)
                        for i in range(len(pre_data)):
                            if i < 2:
                                continue
                            else:
                                date_data[self.fields2[i]] = date_data[self.fields2[i]] - pre_data[self.fields2[i]]
                    all_country_date_data['2020-'+date] = date_data
                return all_country_date_data
        if city == '' and province == '' and country.lower() == 'china':
            all_country_date_data = {}
            if Type == 'accumulated':
                for date in createdb.date_list:
                    if '2020-' + date == Date:
                        break
                    date_data = self.get_data_accumulated('2020-' + date, country, 'province', 'city')
                    country_date_data = {'date': '2020-' + date, 'country': 'China', 'confirmed': 0, 'cured': 0, 'death': 0}
                    country_date_data['confirmed'] += date_data['confirmed']
                    country_date_data['cured'] += date_data['cured']
                    country_date_data['death'] += date_data['death']
                    all_country_date_data['2020-' + date] = country_date_data
                    # province_list = self.get_province_list(Date)
                    # for province in province_list.keys():
                    #     # print(province)
                    #     for city in province_list[province]:
                    #         # 这些数据要删除
                    #         if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                    #             continue
                    #         date_data = self.get_data_accumulated('2020-' + date, country, province, createdb.hp(city))
                    #         country_date_data['confirmed'] += date_data['confirmed']
                    #         country_date_data['cured'] += date_data['cured']
                    #         country_date_data['death'] += date_data['death']
                    # all_country_date_data['2020-' + date] = country_date_data
                return all_country_date_data
            if Type == 'someday':
                for date in createdb.date_list:
                    if '2020-' + date == Date:
                        break
                    date_data = self.get_data_accumulated('2020-' + date, country, 'province', 'city')
                    country_date_data = {'date': '2020-' + date, 'country': 'China', 'confirmed': 0, 'cured': 0, 'death': 0}
                    pre_day = date_fun.getdate('2020-' + date, 1)
                    if pre_day != '2020-01-21':
                        pre_data = self.get_data_accumulated(pre_day, country, 'province', 'city')
                        for i in range(len(pre_data)):
                            if i < 4:
                                continue
                            else:
                                date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                    country_date_data['confirmed'] += date_data['confirmed']
                    country_date_data['cured'] += date_data['cured']
                    country_date_data['death'] += date_data['death']
                    all_country_date_data['2020-' + date] = country_date_data

                    # province_list = self.get_province_list(Date)
                    # for province in province_list.keys():
                    #     for city in province_list[province]:
                    #         # 这些数据要删除
                    #         if createdb.hp(city) == 'daimingquediqu' or createdb.hp(city) == 'People from other cities':
                    #             continue
                    #         date_data = self.get_data_accumulated('2020-' + date, country, province, createdb.hp(city))
                    #         if pre_day != '2020-01-21':
                    #             pre_data = self.get_data_accumulated(pre_day, country, province, createdb.hp(city))
                    #             for i in range(len(pre_data)):
                    #                 if i < 4:
                    #                     continue
                    #                 else:
                    #                     date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                    #         country_date_data['confirmed'] += date_data['confirmed']
                    #         country_date_data['cured'] += date_data['cured']
                    #         country_date_data['death'] += date_data['death']
                    # all_country_date_data['2020-' + date] = country_date_data
                return all_country_date_data
        if city == '' and province == '' and country == '':
            all_country_date_data = {}
            if Type == 'accumulated':
                for date in createdb.date_list:
                    if '2020-' + date == Date:
                        break
                    date_data = self.get_data_accumulated('2020-' + date, 'country', 'province', 'city')
                    country_date_data = {'date': '2020-' + date, 'confirmed': 0, 'cured': 0, 'death': 0}
                    country_date_data['confirmed'] += date_data['confirmed']
                    country_date_data['cured'] += date_data['cured']
                    country_date_data['death'] += date_data['death']
                    all_country_date_data['2020-' + date] = country_date_data
                return all_country_date_data
            if Type == 'someday':

                for date in createdb.date_list:
                    print(date)
                    if '2020-' + date == Date:
                        break
                    date_data = self.get_data_accumulated('2020-' + date, 'country', 'province', 'city')
                    country_date_data = {'date': '2020-' + date, 'confirmed': 0, 'cured': 0, 'death': 0}
                    pre_day = date_fun.getdate('2020-' + date, 1)
                    if pre_day != '2020-01-21':
                        pre_data = self.get_data_accumulated(pre_day, 'country', 'province', 'city')
                        for i in range(len(pre_data)):
                            if i < 4:
                                continue
                            else:
                                date_data[self.fields[i]] = date_data[self.fields[i]] - pre_data[self.fields[i]]
                    country_date_data['confirmed'] += date_data['confirmed']
                    country_date_data['cured'] += date_data['cured']
                    country_date_data['death'] += date_data['death']
                    all_country_date_data['2020-' + date] = country_date_data

                return all_country_date_data
    def register(self, username, password):
        try:
            self.cursor.execute('insert into username values ("%s", "%s")' % (username, password))
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def login(self, username, password):
        sql = 'select username, password from username where username = "{}" AND password = "{}"'.format(username, password)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        if len(results) == 0:
            return False
        else:
            return True

    def update(self, date, area, detail):
        try:
            if 'province' in area.keys() and 'city' in area.keys():
                self.cursor.execute('insert into data values (%s, %s, %s, %s, %s, %s, %s)', (date, str(area['country']), \
                    str(area['province']), str(area['city']), int(detail['confirmed']), int(detail['cured']), int(detail['death'])))
                self.db.commit()
            else:
                self.cursor.execute('insert into data(date, country, confirmed, cured, death) values (%s, %s, %s, %s, %s)', (date, str(area['country']),\
                    int(detail['confirmed']), int(detail['cured']), int(detail['death'])))
                self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def upload(self, date, country, province, city, confirmed = '', cured = '', death = ''):
        if confirmed == '' or cured == '' or death == '':
            print("NULL value")
            return False
        try:
            self.cursor.execute("insert into data(date, country, province, city, confirmed, cured, death) values (%s, %s, %s, %s, %s, %s, %s)",\
                                (date, country, province, city, str(confirmed), str(cured), str(death)))
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def download(self, date, level = True, country='', province='', city='', confirmed=False, cured=False, death=False, addr=''):
        if confirmed == False and cured == False and death == False:
            print('All values deleted')
            return False
        try:
            if country != '' and province != '' and city != '':
                sql = "select * from data where date < '{}' and country = '{}' AND province = '{}' and city = '{}' ".format(
                    date, country, createdb.hp(province), createdb.hp(city))
            elif country != '' and province != '' and city == '' and level == True:
                sql = "select * from data where date < '{}' and province = '{}' and city = 'city'".format(date, createdb.hp(province))
            elif country != '' and province != '' and city == '' and level == False:
                sql = "select * from data where date < '{}' and province = '{}' ".format(date, createdb.hp(province))
            elif country == 'China' and province == '' and city == '' and level == True:
                sql = "select * from data where date < '{}' and country = 'China' and province = 'province' and city = 'city' ".format(date)
            elif country == 'China' and province == '' and city == '' and level == False:
                sql = "select * from data where date < '{}' and country = 'China' ".format(date)
            elif country != 'China' and country != '' and province == '' and city == '':
                sql = "select * from data where date < '{}' and country = '{}' ".format(date, country)
            elif country == '' and province == '' and city == '' and level == True:
                sql = "select * from data where date < '{}' and (country != 'China' or (country = 'China' and province = 'province' and city = 'city'))".format(date)
            elif country == '' and province == '' and city == '' and level == False:
                sql = "select * from data where date < '{}'".format(date)
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            # 插入csv文件
            f = open('{}'.format(addr), 'w', encoding='utf-8', newline='')
            writer = csv.writer(f)
            firstline = ['Date', 'Country', 'Province', 'City']
            if confirmed == True:
                firstline.append('confirmed')
            if cured == True:
                firstline.append('cured')
            if death == True:
                firstline.append('death')
            writer.writerow(firstline)
            for result in results:
                result = list(result)
                result[0] = str(result[0])
                if death == False:
                    del result[6]
                if cured == False:
                    del result[5]
                if confirmed == False:
                    del result[4]
                writer.writerow(result)

        except Exception as e:
            print(e)

    def request_for_csv(self, paras_dict, addr):
        date = paras_dict['date']
        if 'country' in paras_dict['area'].keys():
            country = paras_dict['area']['country']
        else:
            country = ''
        if 'province' in paras_dict['area'].keys():
            province = paras_dict['area']['province']
        else:
            province = ''
        if 'city' in paras_dict['area'].keys():
            city = paras_dict['area']['city']
        else:
            city = ''
        if 'confirmed' in paras_dict['data_type']:
            confirmed = True
        else:
            confirmed = False
        if 'cured' in paras_dict['data_type']:
            cured = True
        else:
            cured = False
        if 'death' in paras_dict['data_type']:
            death = True
        else:
            death = False
        level = paras_dict['level']
        return self.download(date, level, country, province, city, confirmed, cured, death, addr)



if __name__ == "__main__":
    
    test = database()
    # 提取数据
    # print(test.barchart('accumulated', '2020-05-20', 'China', '重庆'))
    # print(test.linechart('accumulated', '2020-05-23'))

    # 注册登录
    # print(test.register("test", "test"))
    # print(test.login("abc", "123"))

    # 插入新数据
    # test.update('2020-03-29', {'country': 'China'}, {'confirmed': 0, 'cured': 0, 'death': 0})
    # test.upload('2020-05-24', 'China', 'Guangdong', 'Guangzhou' , 20, 20)
    # print(test.get_country_list(date))
    # print(test.get_province_list(date))

    # 数据下载
    # test.download('2020-05-01', False, confirmed='Yes', cured='Yes', death='No')
    test.request_for_csv({"date": "2020-05-03", "area": {"country": "China", "province": "广东"},"data_type": ["confirmed", "cured"], "level": True}, '123')