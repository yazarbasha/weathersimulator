'''
To simulate weather data for each city in a random list of cities
Uses internet(site: google api) to fetch geographic data(lat,long,elev) of the cities.
Temperature, humidity and pressure are generated randomly with in the defined range.

Emitted Data:
Location|Position(lat,long,ele)|Localtime|Conditions|Temperature|Pressure|Humidity
* Location is an optional label describing one or more positions,
* Position is a comma-separated triple containing latitude, longitude, and elevation in metres above sea
level,
* Local time is an ISO8601 date time,
* Conditions is either Snow, Rain, Sunny,
* Temperature is in Degree Celcius, 
* Pressure is in hPa, and
* Relative humidity is a %

Sample O/P:
Sydney|-33.86,151.21,39|2015-12-23T05:02:12Z|Rain|+12.5|1004.3|97
Melbourne|-37.83,144.98,7|2015-12-24T15:30:55Z|Snow|-5.3|998.4|55
Adelaide|-34.92,138.62,48|2016-01-03T12:35:37Z|Sunny|+39.4|1114.1|12

Maker: Yazar Basha
Checker:  Yazar Basha
Date: 27-Sep-2017
'''
import datetime
import json
import random
import urllib

class WeatherSimulator(object):
    '''
    Module Name  : weathersimulator
    Class Detail : Used to initialize a list of cities, if no list is passed then use default list,
                   Contains method to get location data and any random date since last 100 days
    '''
    def __init__(self,citylist=[]):
        if len(citylist)==0:
            self.list_of_cities = ['Melbourne','Sydney','Adelaide','Brisbane',
                                   'New Delhi','Chennai','Mumbai','Kolkatta',
                                   'Chicago','New York Metro','San Francisco',
                                   'Singapore','Moscow','Angalakurichi',
                                   'Istanbul','Beijing','London',
                                   'Hyderabad','Barcelona','Coimbatore']

        self.cname = ''
        self.temp  = 0
        self.hum   = 0
        self.pres  = 0
        self.cond  = ''
        self.ele   = ''
        self.lat   = 0.0
        self.lon   = 0.0
        self.time  = ''


    def getEle(self):
        '''
        Parameters: None
        :return: Elevation in Metres
        Uses google api without key to get elevation info based on lat, long
        '''
        url = 'http://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&sensor={sen}'.format(lat=self.lat,lon=self.lon,sen='false')
        data = urllib.urlopen(url)
        response = json.loads(data.read())
        if (str(response['status']) == 'OK'):
            return response['results'][0]['elevation']

    def getLoc(self):
        '''
        Parameters: None
        :return: Lat,Long,Ele (comma separated string)
        Uses google api to get lat ad long information based on city name
        Use proper name of a place
        '''
        url = 'http://maps.googleapis.com/maps/api/geocode/json?address={name}&sensor={sens}'.format(name=self.cname,sens='false')
        response = urllib.urlopen(url).read()
        data = json.loads(response)
        if (str(data['status']) == 'OK'):
            (self.lat, self.lon) = data['results'][0]['geometry']['location'].values()
            self.ele = self.getEle()
        return '%.2f,%.2f,%.0f' % (self.lat, self.lon, self.ele)


    def getTzinfo(self):
        '''
        Parameters: None
        :return: ISODate
        To produce a random date and time in ISO format from last 100 days of current system date
        '''
        return (datetime.datetime.today() - \
                datetime.timedelta(seconds=random.randint(0, 8640000))).isoformat()

    def simulator(self):
        '''
        Parameter:None
        :return: Pipeseparated Strings of weather data in the format
                 Location|Position(lat,long,ele)|Localtime|Conditions|Temperature|Pressure|Humidity
        Simulates random weather data of list of cities
        '''
        cno        = random.sample(range(0,len(self.list_of_cities)),len(self.list_of_cities)) #Random list of numbers without Replacement
        for i in cno:
            self.cname = self.list_of_cities[i]
            self.loc   = self.getLoc()
            self.hum   = random.randint(70, 130) #hum>100 then water condenses *Assumption
            self.pres  = random.randint(913, 1213)#Avg 1013, +/-100 for range
            self.temp  = random.randint(-15, 50)#*Not fair if snows in cheYnnai
            self.time  = self.getTzinfo()
            self.cond  = ''
            if self.temp > 0 and self.hum >= 100:
                self.cond = 'Rain'
            elif self.temp > 0 and self.hum < 100:
                self.cond = 'Sunny'
            elif self.temp < 0 and self.hum < 100:
                self.cond = 'Snow'
            elif self.temp <= 0 and self.hum >= 100:
                self.cond = 'Snow'
            elif self.temp == 0 and self.hum < 100:
                self.cond = 'Sunny'
            elif self.temp == 0 and self.hum > 100:
                self.cond = 'Rain'
            else: self.cond='Unforeseen'
            simulatedata = [self.cname, self.loc, self.time, self.cond, self.temp, self.pres, self.hum]
            print '|'.join(map(str,simulatedata))


if __name__ == "__main__":
    c = WeatherSimulator() #Can pass a different list
    while (1): #
        val=raw_input('Press Y for an iteration of Weather Simulated Date, Else Press anykey to Exit\n')
        if val=='Y' or val=='y':
            try :
                c.simulator()
            except Exception:
                print 'We just crashed, Please try again'
        else:
            print 'Thank you for using  the Simulator!!!'
            exit(0)