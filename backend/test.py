# import pandas as pd
# import numpy as np
# import datetime
# data = pd.read_csv("DXYArea.csv")
# headers = ["date", "country", "province", "city", "confirmed", "cured", "death"]
# a, b, c = [1, 2, 4]
# print(data)
# def _time_helper(date):
#     date = date.split('/')
#     for i in range(len(date)):
#         date[i] = int(date[i])
#     year, month, day = date
#     return datetime.date(year, month, day).isoformat()



# print( _time_helper(data.loc[0]["date"]))

test = {"date":"2020-05-22", "area":{"country":"china", "province":"guangdong"}, "data_type":["confirmed", "cured"], "level":True}
print(type())
