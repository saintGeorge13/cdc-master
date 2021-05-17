# -*- coding: UTF-8 -*- 
from flask import Flask
from flask import request
import db
import json
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"


@app.route('/hotspotmap_json/',methods=["GET"])
def hotspotmap_json():
    try:
        db_ = db.database()
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        # print(params_dict)
        if "type" in params_dict.keys() and "date" in params_dict.keys():
            if params_dict["type"] == "someday":
                # get someday data
                if "country" in params_dict.keys():
                    if "province" in params_dict.keys():
                        # return the data of every city in the province of a particular day
                        data = db_.barchart(type = params_dict["type"], date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                        return_data = dict()
                        return_data["country"] = params_dict["country"]
                        return_data["province"] = params_dict["province"]
                        return_data["detail"] = list()
                        for city_detail in data.values():
                            return_data["detail"].append({"name" : city_detail["city"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                        return json.dumps(return_data)
                    else:
                        if params_dict["country"] == "china":
                            # return the data of every province in the world of a particular day
                            data = db_.barchart(type = params_dict["type"], date = params_dict["date"], country = params_dict["country"])
                            return_data = dict()
                            return_data["country"] = params_dict["country"]
                            return_data["detail"] = list()
                            for city_detail in data.values():
                                return_data["detail"].append({"name" : city_detail["province"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                            return json.dumps(return_data)
                        else:
                            return json.dumps({{"code":0, "message":"失败"}})
                else:
                    # return the data of every country in the world of a particular day
                    data = db_.barchart(type = params_dict["type"], date = params_dict["date"])
                    return_data = dict()
                    return_data["detail"] = list()
                    for city_detail in data.values():
                        return_data["detail"].append({"name" : city_detail["country"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                    return json.dumps(return_data)
                
            elif params_dict["type"] == "accumulated":
                # get accumulated data
                if "country" in params_dict.keys():
                    if "province" in params_dict.keys():
                        # return the data of every city in the province of a particular day
                        data = db_.barchart(type = params_dict["type"], date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                        return_data = dict()
                        return_data["country"] = params_dict["country"]
                        return_data["province"] = params_dict["province"]
                        return_data["detail"] = list()
                        for city_detail in data.values():
                            return_data["detail"].append({"name" : city_detail["city"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                        return json.dumps(return_data)
                    else:
                        if params_dict["country"] == "china":
                            # return the data of every province in the world of a particular day
                            data = db_.barchart(type = params_dict["type"], date = params_dict["date"], country = params_dict["country"])
                            return_data = dict()
                            return_data["country"] = params_dict["country"]
                            return_data["detail"] = list()
                            for city_detail in data.values():
                                return_data["detail"].append({"name" : city_detail["province"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                            return json.dumps(return_data)
                        else:
                            return json.dumps({{"code":0, "message":"失败"}})
                else:
                    # return the data of every country in the world of a particular day
                    data = db_.barchart(type = params_dict["type"], date = params_dict["date"])
                    return_data = dict()
                    return_data["detail"] = list()
                    for city_detail in data.values():
                        return_data["detail"].append({"name" : city_detail["country"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                    return json.dumps(return_data)
            else:
                ##################################################################
                # error param handling return a json explictly informs the error #
                ##################################################################
                return json.dumps({{"code":0, "message":"失败"}})
        else:
            return json.dumps({{"code":0, "message":"失败"}})
    except KeyError as e:
        print(e)
        return json.dumps({{"code":0, "message":"失败"}})






@app.route('/linechart_json/',methods=["GET"])
def linechart_json():
    try:
        db_ = db.database()
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)
        if "date" not in params_dict.keys() or "type" not in params_dict.keys():
            return json.dumps({{"code":0, "message":"失败"}})
        else:
            if params_dict["type"] == "someday":
                if "city" in params_dict.keys() and params_dict["country"] == "china":
                    # return the data of specific city
                    data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"], province = params_dict["province"], city= params_dict["city"])
                    return_data = dict()
                    return_data["date"] = list()
                    return_data["detail"] = list()
                    for date_detail in data.values():
                        return_data["date"].append(date_detail["date"])
                        return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                    return json.dumps(return_data)
                if "province" in params_dict.keys() and params_dict["country"] == "china":
                    # return the data of specific province
                    data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                    return_data = dict()
                    return_data["date"] = list()
                    return_data["detail"] = list()
                    for date_detail in data.values():
                        return_data["date"].append(date_detail["date"])
                        return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                    return json.dumps(return_data)
                    
                if "country" in params_dict.keys():
                    # return the data of specific country
                    data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"])
                    return_data = dict()
                    return_data["date"] = list()
                    return_data["detail"] = list()
                    for date_detail in data.values():
                        return_data["date"].append(date_detail["date"])
                        return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                    return json.dumps(return_data)
            elif params_dict["type"] == "accumulated":
                if "city" in params_dict.keys() and params_dict["country"] == "china":
                    # return the data of specific city
                    data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"], province = params_dict["province"], city= params_dict["city"])
                    return_data = dict()
                    return_data["date"] = list()
                    return_data["detail"] = list()
                    for date_detail in data.values():
                        return_data["date"].append(date_detail["date"])
                        return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                    return json.dumps(return_data)
                if "province" in params_dict.keys() and params_dict["country"] == "china":
                    # return the data of specific province
                    data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                    return_data = dict()
                    return_data["date"] = list()
                    return_data["detail"] = list()
                    for date_detail in data.values():
                        return_data["date"].append(date_detail["date"])
                        return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                    return json.dumps(return_data)
                    
                if "country" in params_dict.keys():
                    # return the data of specific country
                    data = db_.linechart(Type = params_dict["type"], Date = params_dict["date"], country = params_dict["country"])
                    return_data = dict()
                    return_data["date"] = list()
                    return_data["detail"] = list()
                    for date_detail in data.values():
                        return_data["date"].append(date_detail["date"])
                        return_data["detail"].append([date_detail["confirmed"], date_detail["cured"], date_detail["death"]])
                    return json.dumps(return_data)
            else:
                return json.dumps({{"code":0, "message":"失败"}})
    except KeyError as e:
        print(e)
        return json.dumps({{"code":0, "message":"失败"}})





@app.route('/barchart_json/',methods=["GET"])
def barchart_json():
    try:
        db_ = db.database()
        # get the params from get
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)

        if "type" in params_dict.keys() and "date" in params_dict.keys():
            if params_dict["type"] == "someday":
                # get someday data
                if "country" in params_dict.keys():
                    if "province" in params_dict.keys():
                        # return the data of every city in the province of a particular day
                        data = db_.barchart(type = params_dict["type"], date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                        return_data = dict()
                        return_data["country"] = params_dict["country"]
                        return_data["province"] = params_dict["province"]
                        return_data["detail"] = list()
                        for city_detail in data.values():
                            return_data["detail"].append({"name" : city_detail["city"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                        return json.dumps(return_data)
                    else:
                        if params_dict["country"] == "china":
                            # return the data of every province in the world of a particular day
                            data = db_.barchart(type = params_dict["type"], date = params_dict["date"], country = params_dict["country"])
                            return_data = dict()
                            return_data["country"] = params_dict["country"]
                            return_data["detail"] = list()
                            for city_detail in data.values():
                                return_data["detail"].append({"name" : city_detail["province"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                            return json.dumps(return_data)
                        else:
                            return json.dumps({{"code":0, "message":"失败"}})
                else:
                    # return the data of every country in the world of a particular day
                    data = db_.barchart(type = params_dict["type"], date = params_dict["date"])
                    return_data = dict()
                    return_data["detail"] = list()
                    for city_detail in data.values():
                        return_data["detail"].append({"name" : city_detail["country"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                    return json.dumps(return_data)
                
            elif params_dict["type"] == "accumulated":
                # get accumulated data
                if "country" in params_dict.keys():
                    if "province" in params_dict.keys():
                        # return the data of every city in the province of a particular day
                        data = db_.barchart(type = params_dict["type"], date = params_dict["date"], country = params_dict["country"], province = params_dict["province"])
                        return_data = dict()
                        return_data["country"] = params_dict["country"]
                        return_data["province"] = params_dict["province"]
                        return_data["detail"] = list()
                        for city_detail in data.values():
                            return_data["detail"].append({"name" : city_detail["city"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                        return json.dumps(return_data)
                    else:
                        if params_dict["country"] == "china":
                            # return the data of every province in the world of a particular day
                            data = db_.barchart(type = params_dict["type"], date = params_dict["date"], country = params_dict["country"])
                            return_data = dict()
                            return_data["country"] = params_dict["country"]
                            return_data["detail"] = list()
                            for city_detail in data.values():
                                return_data["detail"].append({"name" : city_detail["province"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                            return json.dumps(return_data)
                        else:
                            return json.dumps({{"code":0, "message":"失败"}})
                else:
                    # return the data of every country in the world of a particular day
                    data = db_.barchart(type = params_dict["type"], date = params_dict["date"])
                    return_data = dict()
                    return_data["detail"] = list()
                    for city_detail in data.values():
                        return_data["detail"].append({"name" : city_detail["country"], "comfirmed" : city_detail["comfirmed"], "cured" :city_detail["cured"], "death" : city_detail["death"]})
                    return json.dumps(return_data)
            else:
                ##################################################################
                # error param handling return a json explictly informs the error #
                ##################################################################
                return json.dumps({{"code":0, "message":"失败"}})
        else:
            return json.dumps({{"code":0, "message":"失败"}})
    except KeyError as e:
        print(e)
        return json.dumps({{"code":0, "message":"失败"}})




# the above is correctly structured
# the following has not been correctly structured yet

@app.route('/login/', methods=['GET'])
def login():
    if request.method == 'GET':
        params = request.args.items()
        params_dict = dict()
        for param in params:
            params_dict[param[0]] = param[1]
        print(params_dict)
        if valid_login(params_dict['username'], params_dict['password']):
            return json.dumps({{"code":1, "message":"成功"}})
        else:
            return json.dumps({{"code":0, "message":"失败"}})
    else:
        return json.dumps({{"code":0, "message":"失败"}})

def valid_login(username, password):
    db_ = db.database()
    return db_.login(username, password)


@app.route('/data_update/', methods=['POST'])
def data_update():
    db_ = db.database()
    if request.method == 'POST':
        data = json.dumps(request.get_json())
        try:
            data = data["data"]
            for piece in data:
                year = piece["date"]["year"]
                month = piece["date"]["month"]
                day = piece["date"]["day"]
                area = piece["area"]# a dict with key country, maybe province and city
                detail = piece["datail"]# a dict with key "confirmed", "deaths", "recovered"
                
                date = str(year) + '-' + str(month) + '-' + str(day)
            if db_.update(date, area, detail):
                return json.dumps({{"code":1, "message":"成功"}})
            else:
                return json.dumps({{"code":0, "message":"失败"}})
        except Exception as e:
            print(e)
            return json.dumps({{"code":0, "message":"失败"}})
        
    
    else:
        return json.dumps({"code" : 0, "message":"失败"})


@app.route('/register/', methods=['POST'])
def register():
    if request.method == 'POST':
        data = json.dumps(request.get_json())
        try:
            username = data['username']
            password = data['password']
        except Exception as e:
            print(e)
            json.dumps({{"code":0, "message":"失败"}})
        if register_(username, password):
            return json.dumps({{"code":1, "message":"成功"}})
        else:
            return json.dumps({{"code":0, "message":"失败"}})
    else:
        return json.dumps({{"code":0, "message":"失败"}})


def register_(username, password):
    db_ = db.database()
    return db_.register(username, password)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
