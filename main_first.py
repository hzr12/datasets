import requests
import datetime
import time
import pandas as pd

trainNumbers = ['G5003']
result_lists = []
headers = {
    'Host': 'rail.moefactory.com',
    'Origin': 'https://rail.moefactory.com',
    'Referer': 'https://rail.moefactory.com/train/number',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
}
url = 'https://rail.moefactory.com/api/trainNumber/query'
time_url = 'https://rail.moefactory.com/api/trainDetails/queryTrainDelayDetails'
def get_raw_date(i=1):
    raw_date = datetime.date.today().strftime("%Y%m%d")
    return int(raw_date) - i
def format_date(date):
    date_str = str(date)
    date_obj = datetime.datetime.strptime(date_str, "%Y%m%d") #将YYYYMMDD格式转换为YYYY-MM-DD
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def get_result_data(num_json_data, time_json_data):
    for i in range(num_json_data):
        if i == 0:
            result = {
                '车次ID': time_json_data['data'][i]['trainNumber'],
                '车站名': time_json_data['data'][i]['stationName'],
                '到达日期': time_json_data['data'][i]['departureDate'],
                '到达时间': time_json_data['data'][i]['departureTime'],
                '出发日期': time_json_data['data'][i]['departureDate'],
                '出发时间': time_json_data['data'][i]['departureTime'],
                '延误分钟': time_json_data['data'][i]['delayMinutes'],
                # 'distance': time_json_data['data'][i]['distance']
            }
            result_lists.append(result)
        else:
            result = {
                '车次ID': time_json_data['data'][i]['trainNumber'],
                '车站名': time_json_data['data'][i]['stationName'],
                '到达日期': time_json_data['data'][i]['arrivalDate'],
                '到达时间': time_json_data['data'][i]['arrivalTime'],
                '出发日期' : time_json_data['data'][i]['departureDate'],
                '出发时间' : time_json_data['data'][i]['departureTime'],
                '延误分钟' : time_json_data['data'][i]['delayMinutes'],
                # 'distance' : time_json_data['data'][i]['distance']
            }
            result_lists.append(result)

def get_data_json(url, headers, data):
    response = requests.post(url=url, headers=headers,data=data)
    json_data = response.json()
    return json_data
date = get_raw_date(2)
for trainNumber in trainNumbers:
    get_data = {
        'date': date,
        'TrainNumber': trainNumber
    }
    get_json_data = get_data_json(url=url, headers=headers, data=get_data)
    start_station = get_json_data['data']['data'][0]['beginStationName']
    end_station = get_json_data['data']['data'][0]['endStationName']
    time_data = {
        'date': date,
        'TrainNumber': trainNumber,
        'fromStationName' : start_station,
        'toStationName' : end_station
    }
    time_json_data = get_data_json(url=time_url, headers=headers, data=time_data)
    num_json_data=len(time_json_data['data'])
    formatted_date = format_date(date)
    get_result_data(num_json_data, time_json_data)
df = pd.DataFrame(result_lists)
df.to_csv(f'dataset/{date}_{trainNumbers[0]}.csv', index=False)
