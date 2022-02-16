import datetime
import time


class DateUtilities:

    @staticmethod
    def getCurrentHour():
        now = datetime.datetime.now()
        return now.hour;

    def getTodayDate(self):
        today = datetime.date.today()
        return today;

    def getWeekDay(self):
        weekday = datetime.date.today().weekday()
        return weekday


    def getYYMM(self):
        now = datetime.datetime.now()
        year_month = now.strftime("%Y-%m");
        return year_month

    def currentTimeMills(self):
        millis = int(round(time.time() * 1000))
        return millis;

    def getTodayTimeStamp(self):
        now = datetime.datetime.now()
        return now;

    def getTodayHourMin(self):
        now = datetime.datetime.now()
        hourMin = now.strftime("%Y-%m-%d %H:%M");
        return hourMin;

    def getTodayCurrentHour(self):
        now = datetime.datetime.now()
        hour = now.strftime("%Y-%m-%d %H");
        return hour;

    @staticmethod
    def getTodayConcatenatedDate():
        now = datetime.datetime.now()
        hour = now.strftime("%Y%m%d");
        return hour;

    def getCurrentDay(self):
        now = datetime.datetime.now()
        return now.day;

    def getCurrentMin(self):
        now = datetime.datetime.now()
        return now.minute;

    def getCurrentSeconds(self):
        now = datetime.datetime.now()
        return now.second;

    def getCurrentMicroseconds(self):
        now = datetime.datetime.now()
        return now.microsecond;

    def getCurrentMonth(self):
        now = datetime.datetime.now()
        return now.month;

    def getCurrentYear(self):
        now = datetime.datetime.now()
        return now.year;

    def parseDateTimeToDate(self, date_time_str):
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        return date_time_obj.date();

    def parseDateTimeToDate_two(self, date_time_str):
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        return date_time_obj.date();

    def parseDateTimeToTime(self, date_time_str):
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        return date_time_obj.time();

    def parseDateTimeToDate_(self, date_time_str):
        # date_time_str = 'Jun 28 2018  7:40AM'
        date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')
        return date_time_obj.date();

    def parseDateTimeToTime_(self, date_time_str):
        # date_time_str = 'Jun 28 2018  7:40AM'
        date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')
        return date_time_obj.time();

    def getPreviousDate(self, _days):
        yesterday = datetime.date.today() - datetime.timedelta(_days)
        return yesterday.strftime('%Y-%m-%d');

    def getPreviousHour(self):
        # import timedelta
        last_hour_date_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        return last_hour_date_time.strftime('%Y-%m-%d %H')

    def getPreviousMinutes(self, minutes):
        last_x_minutes = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        return last_x_minutes.strftime('%Y-%m-%d %H:%M:%S.%f')

    def getSecondsDifference(self, startdate, enddate):
        from datetime import datetime
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime(startdate, fmt)
        d2 = datetime.strptime(enddate, fmt)
        delta = d2 - d1
        return delta.total_seconds()

    def getTodayHourMinSec(self):
        now = datetime.datetime.now()
        hourMin = now.strftime("%Y-%m-%d %H:%M:%S");
        return hourMin;
