import requests
import json
from keyMsg import keyMsg

def sendMessage(accessToken,user,config,msg):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(accessToken)
    cityInfo,weatherInfo,tempInfo = msg.weather()
    years,months,days,delta_days = msg.loveDays()
    if days == 0:
        if months == 0:
            year,yeartxt = f"{years}","年啦"
            month,monthtxt = "",""
            day,daytxt= "",""
        else:
            year,yeartxt = f"{years}","年"
            month,monthtxt = f"{months}","个月啦"
            day,daytxt= "",""
    else:
        year,yeartxt = "",""
        month,monthtxt = "",""
        day,daytxt= f"{delta_days}","天"
    ywBirthday = msg.toBrithday()
    if ywBirthday == 0:
        birthdayText = "阅宝宝生日快乐！"
    else:
        birthdayText = f"阅宝宝生日{ywBirthday}天"
    Holiday = msg.toHoliday()
    if Holiday == 0:
        HolidayText = "今天是休息日，好好放松一下！"
    else:
        HolidayText = f"休息日还有{Holiday}天"
    bfMoneyDay = msg.moneyDays(5)
    ywMoneyDay = msg.moneyDays(15)
    if bfMoneyDay == 0:
        MoneyText = "今天帆小生发工资啦！"
    elif ywMoneyDay == 0:
        MoneyText = "今天阅宝宝发工资啦！"
    else:
        MoneyText = f"发工资倒计时：帆小生{bfMoneyDay}天，阅宝宝{ywMoneyDay}天"
    to111 = -msg.calDays("2023-1-11")
    to111 = f"{to111}"
    data = {
        "touser": user,
        "template_id": config["templateID"],
        #"url": "http://baidu.com/",    
        "topcolor": "#FF0000",
        "data": {
            "today": {
                "value": msg.today(),
                "color": "#00B271"
                },
            "year":{
                "value": year,
                "color": "#479AC7"
                },
            "yeartxt":{
                "value": yeartxt,
                "color": "#000000"
                },
            "month":{
                "value": month,
                "color": "#479AC7"
                },
            "monthtxt":{
                "value": monthtxt,
                "color": "#000000"
                },
            "day":{
                "value": day,
                "color": "#479AC7"
                },
            "daytxt":{
                "value": daytxt,
                "color": "#000000"
                },
            "city":{
                "value": cityInfo,
                "color": "#B45B3E"
                },
            "weather":{
                "value": weatherInfo,
                "color": "#B45B3E"
                },
            "temperature":{
                "value": tempInfo,
                "color": "#B45B3E"
                },
            "ywBirthday":{
                "value": birthdayText,
                "color": "#B45B3E"
                },
            "Holiday":{
                "value": HolidayText,
                "color": "#B45B3E"
                },
            "to111":{
                "value": to111,
                "color": "#B45B3E"
                },
            "MoneyText":{
                "value": MoneyText,
                "color": "#00B271"
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
    with open("config.txt", encoding="utf-8") as f:
        config = eval(f.read())

    appID = config["appID"]
    appSecret = config["appsecret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(appID, appSecret))
    accessToken = requests.get(post_url).json()['access_token']
    msg = keyMsg()
    
    for user in config["users"]:
        sendMessage(accessToken,user,config,msg)

    input('Press Enter to exit...')
    