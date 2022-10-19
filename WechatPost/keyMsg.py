import datetime
import requests
import json
import sxtwl
from chinese_calendar import is_holiday, is_workday

class keyMsg():
    def __init__(self):
        self.sysday = datetime.date.today()  # 只获取日期
        #self.sysday = datetime.date(2022,5,30)  # 只获取日期

    # 通过天气api获取天气信息
    def weather(self):
        city = '101190101'#南京
        url = 'http://t.weather.sojson.com/api/weather/city/'+city
        response = requests.get(url)
        allWeatherInfo = response.json()
        # 城市
        cityInfo = allWeatherInfo['cityInfo']['city']
        # 天气
        weatherInfo = allWeatherInfo['data']['forecast'][0]
        # 温度
        str_tem_low = weatherInfo['low'].split(' ')
        str_tem_high = weatherInfo['high'].split(' ')
        tempInfo = f"{str_tem_low[1]}~{str_tem_high[1]}"
        return cityInfo,weatherInfo['type'],tempInfo

    #获取当前时间信息
    def today(self):
        # 今日日期与星期数
        week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        weekday = self.sysday.isoweekday()  # 获取周几
        return f"{self.sysday.year}年{self.sysday.month}月{self.sysday.day}日{week[weekday-1]}"

    # 计算在一起的时长
    def loveDays(self):
        # 获得天数
        loveday = datetime.date(2019, 5, 30)
        delta_days = (self.sysday - loveday).days
        # 获得年月
        months = (self.sysday.year - loveday.year)*12 + (self.sysday.month - loveday.month)
        years = months//12
        months = months%12
        # 获得日，暂未使用
        next_month_oneday = self.sysday.replace(day=28) + datetime.timedelta(days=4)  # 获取到下个月的某天
        next_month_oneday_days = datetime.timedelta(days=next_month_oneday.day)  # 获取该天在该月的天数
        this_month_final = next_month_oneday - next_month_oneday_days  # next_month_oneday减去自身的天数，即可得到本月的月底最后一天
        if this_month_final.day <= 30:
            days = self.sysday.day - this_month_final.day
        else:
            days = self.sysday.day - 30
        if days<0:
            months = months - 1
            days = self.sysday.day
            last_month_final = self.sysday - datetime.timedelta(days=self.sysday.day)
            if last_month_final.day == 31:
                days = days+1
        return [years,months,days,delta_days]

    # 计算在一起的时长
    def calDays(self,targetDay):
        # 获得天数
        tmp = targetDay.split("-")
        Tday = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
        return (self.sysday - Tday).days

    # 计算发工资天数
    def moneyDays(self,moneyday):
        tempday = datetime.date(self.sysday.year, self.sysday.month, moneyday)
        while is_holiday(tempday):
            tempday = tempday - datetime.timedelta(days=1)
        to_money_day = (tempday-self.sysday).days
        if to_money_day < 0:
            tempyear = self.sysday.year
            tempmonth = self.sysday.month+1
            if tempmonth>12:
                tempmonth = 1
                tempyear = tempyear+1
            tempday = datetime.date(tempyear, tempmonth, moneyday)
            while is_holiday(tempday):
                tempday = tempday - datetime.timedelta(days=1)
            to_money_day = (tempday-self.sysday).days
        return to_money_day

    # 计算生日
    def toBrithday(self):
        #生日期限
        yw_birthday_lunar = sxtwl.fromLunar(self.sysday.year, 4, 11)
        yw_birthday_solar = datetime.date(yw_birthday_lunar.getSolarYear(), 
                                        yw_birthday_lunar.getSolarMonth(),
                                        yw_birthday_lunar.getSolarDay())
        to_yw_birthday = (yw_birthday_solar-self.sysday).days
        if to_yw_birthday < 0:
            yw_birthday_lunar = sxtwl.fromLunar(self.sysday.year+1, 4, 11)
            yw_birthday_solar = datetime.date(yw_birthday_lunar.getSolarYear(), 
                                            yw_birthday_lunar.getSolarMonth(),
                                            yw_birthday_lunar.getSolarDay())
            to_yw_birthday = (yw_birthday_solar-self.sysday).days
        return to_yw_birthday

    # 计算休息日
    def toHoliday(self):
        to_holiday = 0
        tempday = self.sysday
        while is_workday(tempday):
            to_holiday = to_holiday+1
            tempday = tempday + datetime.timedelta(days=1)
        return to_holiday

    # 计算农历
    def lunarDay(self):
        #今日农历
        ymc = [u"正", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十", u"十一", u"十二",]
        rmc = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十",
            u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九",
            u"二十", u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", 
            u"廿九", u"三十", u"卅一"]
        Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        day = sxtwl.fromSolar(self.sysday.year, self.sysday.month, self.sysday.day)
        if sxtwl.getRunMonth(self.sysday.year) == day.getLunarMonth():
            a = "润" + ymc[day.getLunarMonth()-1] + "月" + rmc[day.getLunarDay()] + "日"
        else:
            a = ymc[day.getLunarMonth()-1] + "月" + rmc[day.getLunarDay()] + "日"
        yTG = day.getYearGZ()
        mTG = day.getMonthGZ()
        dTG = day.getDayGZ()
        c = Gan[yTG.tg] + Zhi[yTG.dz] + "年" + Gan[mTG.tg] + Zhi[mTG.dz] + "月" + Gan[
            dTG.tg] + Zhi[dTG.dz] + "日"
        return '农历' + a + ', ' + c
         