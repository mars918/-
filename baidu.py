#12306火车票查询
#解析json
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
from .stations import station_dict
'''
获得12306城市代码的数据
文件名：parse_station.py
'''
#关闭https证书验证警告
requests.packages.urllib3.disable_warnings()
stationlist_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9042'
r = requests.get(stationlist_url, verify=False)
pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
result = re.findall(pattern,r.text)
station = dict(result)
#print(station)

'''
分析json
调用接口获取
https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=2018-02-01&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=BJP&purpose_codes=ADULT
参数：train_date,from_station,to_station,purpose_codes
'''
#城市名代码查询字典
#key：城市名 value：城市代码
from .stations import stations_dict
code_dict = {v: k for k, v in station_dict.item()}
#生产新的字典
#把字典传递给json
def get_query_url(text):
    args = str(text).split('')
    try:
        data = args[1]
        from_station_name = args[2]
        to_station_name = args[3]
        from_station=stations_dict[from_station_name]
        to_station = stations_dict[to_station_name]
    except:
        date, from_station, to_station='__', '__', '__'

    #api url 构造
    url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT').format(date, from_station, to_station)
    print (url)

    return url
#查询火车信息，
#返回 信息查询列表
def query_train_info(url):
    info_list = []
    try:
        r = requests.get(url, verify=False)
        #获取返回的接送数据里的data字段的result结果
        raw_trains = r.json()['data']['result']

        for raw_trains in raw_trains:
            #查询每一列车的信息
            data_list = raw_trains.split('|')
            #车次号码
            train_nu = data_list[3]
            #出发站
            from_station_code = data_list[6]
            from_station_name = code_dict[from_station_code]
            #终点站
            to_station_code = data_list[7]
            to_station_name = code_dict[to_station_code]
            #出发时间
            start_time = data_list[8]
            #到达时间
            arrive_time = data_list[9]
            #总耗时
            time_fucked_up = data_list[10]
            #一等座
            first_
