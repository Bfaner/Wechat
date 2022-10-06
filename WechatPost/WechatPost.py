# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 16:24:39 2022

@author: BFaner
"""

import requests
from urllib import request, parse
import json
import datetime

#通过天气api获取天气信息
def get_weather():
    city = '101190101'#南京
    url = 'http://t.weather.sojson.com/api/weather/city/'+city
    santence = requests.get(url)
    allWeatherInfo = santence.json()
    cityInfo = allWeatherInfo['cityInfo']['city']
    weatherInfo = allWeatherInfo['data']['forecast'][0]
    return cityInfo,weatherInfo

#获取当前时间信息
def get_date_txt():
    # 发送内容 今日日期与星期数
    sysdate = datetime.date.today()  # 只获取日期
    now_time = datetime.datetime.now()  # 获取日期加时间
    week_day = sysdate.isoweekday()  # 获取周几
    week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    text_date = '现在是' + str(now_time)[0:16] + ',' + week[week_day -1 ]
    return text_date

#计算在一起的时长
def get_love_days():
    loveday = datetime.date(2019, 5, 30)
    sysdate = datetime.date.today()  # 只获取日期
    delta_days = sysdate.__sub__(loveday)
    str_delta_days = str(delta_days)
    split_str_days = str_delta_days.split(' ')
    return split_str_days[0]

#产生发送信息
def get_send_text(time):
    text = "\n"
    if time == "morning":
         cityInfo,weatherInfo = get_weather()
         text_date = get_date_txt()
         love_days = get_love_days()
         text = text + "阅宝宝，早上好\n"
         text = text + f"    {text_date}，新的一天更加爱你~\n"
         text = text + f"    在一起已经{love_days}天啦\n"
         text = text + f"    {cityInfo}的天气:{weatherInfo['type']}\n"
         text = text + f"    {weatherInfo['notice']}\n"
    return text

#访问喵提醒，发送微信消息
class Message(object):
    def __init__(self,id,text):
        self.id = id
        self.text = text
    def push(self):
        # 重要，在id中填写自己绑定的id
        page = request.urlopen("http://miaotixing.com/trigger?" + parse.urlencode({"id": self.id, "text": self.text, "type": "json"}))
        result = page.read()
        jsonObj = json.loads(result)
        if (jsonObj["code"] == 0):
            print("\nReminder message was sent successfully")
        else:
            print("\nReminder message failed to be sent，wrong code：" + str(jsonObj["code"]) + "，describe：" + jsonObj["msg"])

#喵提醒发送信息
def send_message(name,text):
    if name == "bf":
        id = "tDajvbH"
    elif name =="yw":
        id = "t0iPmv1" 
    message = Message(id,text)
    message.push() # 完成推送

#获取微信的token
def get_access_token():
    # appId
    app_id = "wxcccc5fa80f2d8249"
    # appSecret
    app_secret = "b4aef470932446bc7fc2569388082def"
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    access_token = requests.get(post_url).json()['access_token']
    #print(access_token)
    return access_token

def send_wx_message(access_token):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    cityInfo,weatherInfo = get_weather()
    text_date = get_date_txt()
    love_days = get_love_days()
    data = {
        "touser": "oJHSd6SLTZYBCTgX0nLar02AZ2GQ",
        #"touser": "oJHSd6Ug2efvFSzEmDi1Pf4CoXNU",
        #"template_id": "QxMDfCj_wKV5sjmnkE9eMb0VS5gLJvpFs_jUN5fOg3g",
        "template_id": "AnLzJcw5l8WHCtbLfjEiY9HzymnK0jokjIXgZvglRy0",
        #"url": "http://baidu.com/",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": text_date + "新的一天更加爱你~",
                "color": "#00FFFF"
                },
            "loveday":{
                "value": "我们在一起已经" + love_days +"天啦",
                "color": "#00FF00"
                },
            "weather":{
                "value": cityInfo + "的天气:" + weatherInfo["type"],
                "color": "#ED9121"
                },
            "weathernote":{
                "value": weatherInfo['notice'],
                "color": "#FF0000"
                }
            }
        }
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

def send_wx_message_2(access_token):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    cityInfo,weatherInfo = get_weather()
    text_date = get_date_txt()
    love_days = get_love_days()
    data = {
        "touser": "oJHSd6Ug2efvFSzEmDi1Pf4CoXNU",
        "template_id": "8Q35pmDCooY_i2LUpSWIrLpSLd1TqDpv8eyeIv6e704",
        "topcolor": "#FF0000",
        "data": {
            "letter": {
                "value": "Hello",
                "color": "#00FFFF"
                }
            }
        }
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

#主函数
if __name__ == '__main__':
    text = get_send_text("morning")
    #send_message("bf",text)
    #send_message("yw",text)
    
    # 获取accessToken
    accessToken = get_access_token()
    send_wx_message_2(accessToken)
    
    #input('Press Enter to exit...')

