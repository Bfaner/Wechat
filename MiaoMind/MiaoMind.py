# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 22:45:39 2022

@author: BFaner
"""

import requests
import datetime,sxtwl
from chinese_calendar import is_holiday, is_workday

#获取当前时间信息
def get_date_txt():
    #今日日期
    today = datetime.date.today()  # 只获取日期
    date_text = '今天是'+str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日'
    #今日星期
    week_day = today.isoweekday()  # 获取周几
    week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    date_text = date_text + week[week_day-1] + ', '
    date_text = date_text + '新的一天心情好好，今天更加爱你哦~\n'
    return date_text

def get_lunar_day():
    today = datetime.date.today()  # 只获取日期
    ldate_text = ''
    #今日农历
    ymc = [u"正", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十", u"十一", u"十二",]
    rmc = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十",
           u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九",
           u"二十", u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", 
           u"廿九", u"三十", u"卅一"]
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    day = sxtwl.fromSolar(today.year, today.month, today.day)
    if sxtwl.getRunMonth(today.year) == day.getLunarMonth():
        a = "润" + ymc[day.getLunarMonth()-1] + "月" + rmc[day.getLunarDay()] + "日"
    else:
        a = ymc[day.getLunarMonth()-1] + "月" + rmc[day.getLunarDay()] + "日"
    yTG = day.getYearGZ()
    mTG = day.getMonthGZ()
    dTG = day.getDayGZ()
    c = Gan[yTG.tg] + Zhi[yTG.dz] + "年" + Gan[mTG.tg] + Zhi[mTG.dz] + "月" + Gan[
        dTG.tg] + Zhi[dTG.dz] + "日"
    #date_text = date_text + '农历' + a + ', ' + c + '\n'
    ldate_text = ldate_text + '今天是农历' + a + '\n'
    return ldate_text

def get_sdate_txt():
    today = datetime.date.today()  # 只获取日期
    sdate_text = ''
    #生日期限
    yw_birthday_lunar = sxtwl.fromLunar(today.year, 4, 11)
    yw_birthday_solar = datetime.date(yw_birthday_lunar.getSolarYear(), 
                                      yw_birthday_lunar.getSolarMonth(),
                                      yw_birthday_lunar.getSolarDay())
    to_yw_birthday = (yw_birthday_solar-today).days
    if to_yw_birthday == 0:
        sdate_text = sdate_text + '\n祝宝宝生日快乐！！！\n'
    elif to_yw_birthday > 0:
        sdate_text = sdate_text + '距离宝宝生日还有' + str(to_yw_birthday) + '天\n'
    else:
        yw_birthday_lunar = sxtwl.fromLunar(today.year+1, 4, 11)
        yw_birthday_solar = datetime.date(yw_birthday_lunar.getSolarYear(), 
                                          yw_birthday_lunar.getSolarMonth(),
                                          yw_birthday_lunar.getSolarDay())
        to_yw_birthday = (yw_birthday_solar-today).days
        sdate_text = sdate_text + '距离宝宝生日还有' + str(to_yw_birthday) + '天\n'
    #判断节假日还有几天
    to_holiday = 0
    tempday = today
    while is_workday(tempday):
        to_holiday = to_holiday+1
        tempday = tempday + datetime.timedelta(days=1)
    if to_holiday == 0:
        sdate_text = sdate_text + '今天是休息日，好好放松一下吧\n'
    else:
        sdate_text = sdate_text + f'距离休息日还有{to_holiday}天\n'
    #判断还有几天发工资
    tempday = datetime.date(today.year, today.month, 5)
    while is_holiday(tempday):
        tempday = tempday - datetime.timedelta(days=1)
    to_money_day = (tempday-today).days
    if to_money_day < 0:
        tempyear = today.year
        tempmonth = today.month+1
        if tempmonth>12:
            tempmonth = 1
            tempyear = tempyear+1
        tempday = datetime.date(tempyear, tempmonth, 5)
        while is_holiday(tempday):
            tempday = tempday - datetime.timedelta(days=1)
            to_money_day = (tempday-today).days
    sdate_text = sdate_text + f'距离白帆发工资还有{to_money_day}天\n'
    return sdate_text

#计算在一起的时长
def get_love_days():
    #获得天数
    loveday = datetime.date(2019, 5, 30)
    today = datetime.date.today()  
    delta_days = (today - loveday).days
    #获得年月日
    months = (today.year - loveday.year)*12 + (today.month - loveday.month)
    next_month_oneday = today.replace(day=28) + datetime.timedelta(days=4)  # 获取到下个月的某天
    next_month_oneday_days = datetime.timedelta(days=next_month_oneday.day)  # 获取该天的天数
    this_month_final = next_month_oneday - next_month_oneday_days  # next_month_oneday减去自身的天数，即可得到本月的月底最后一天
    if this_month_final.day <= 30:
        days = today.day - this_month_final.day
    else:
        days = today.day - 30
    if days<0:
        months = months - 1
        days = today.day
        last_month_final = today - datetime.timedelta(days=today.day)
        if last_month_final.day == 31:
            days = days+1
    years = months//12
    months = months%12
    #输出文本
    if days != 0:
        if months != 0:
            loveday_text =  f"在一起{years}年{months}个月{days}天"
        else:
            loveday_text =  f"在一起{years}年零{days}天"
    else:
        if months != 0:
            loveday_text =  f"在一起{years}年{months}个月啦，这个月也在好好爱你呀~"
        else:
            loveday_text =  f"\n我们在一起的{years}年啦!!!\n"
    lovedays_text = f"我们在一起{delta_days}天啦~\n"
    return loveday_text, lovedays_text

#通过天气api获取天气信息
def get_weather():
    city = '101190101'#南京
    url = 'http://t.weather.sojson.com/api/weather/city/'+city
    response = requests.get(url)
    allWeatherInfo = response.json()
    cityInfo = allWeatherInfo['cityInfo']['city']
    weatherInfo = allWeatherInfo['data']['forecast'][0]
    return cityInfo,weatherInfo

#获取一句情话
def get_love_words():
    url = 'https://v2.alapi.cn/api/qinghua?token=Zie0VhPyt6tf3sCB'
    response = requests.get(url)
    LoveWordInfo = response.json()
    LoveWord = LoveWordInfo['data']['content']
    return LoveWord

#产生发送信息
def get_send_text(time):
    text = "\n"
    if time == "morning":
         cityInfo,weatherInfo = get_weather()
         date_text = get_date_txt()
         loveday_text, lovedays_text = get_love_days()
         #LoveWord = get_love_words()
         str_tem_low = weatherInfo['low'].split(' ')
         str_tem_high = weatherInfo['high'].split(' ')
         text = text + "早安呀，阅宝宝\n\n"
         text = text + f"{date_text}"
         text = text + f"{lovedays_text}"
         text = text + f"{cityInfo}的天气:{weatherInfo['type']},"
         text = text + f"气温:{str_tem_low[1]}~{str_tem_high[1]}"
         #text = text + f"{weatherInfo['notice']}\n"
         
         sdate_text = get_sdate_txt()
         ldate_text = get_lunar_day()
         text = text + "\n\n要记得哦~\n"
         text = text + ldate_text
         text = text + f"{loveday_text}\n"
         text = text + f"{sdate_text}"
        # text = text + f"    {LoveWord}\n"
    return text

#访问喵提醒，发送微信消息
class Message(object):
    def __init__(self,id,text):
        self.id = id
        self.text = text
    def push(self):
        # 重要，在id中填写自己绑定的id
        url = 'http://miaotixing.com/trigger?id='+self.id+'&text='+self.text
        response = requests.get(url)
        # print(response.text)
        # print(url)

#喵提醒发送信息
def send_message(name,text):
    if name == "bf":
        id = "tDajvbH"
    elif name =="yw":
        id = "t0iPmv1" 
    message = Message(id,text)
    message.push() # 完成推送

#主函数
if __name__ == '__main__':
    text = get_send_text("morning")
    send_message("bf",text)
    send_message("yw",text)
    
    input('Press Enter to exit...')
