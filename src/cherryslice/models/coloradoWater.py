'''
Created on Jun 15, 2010

@author: nick
'''
import suds.client
import math
from cherryslice.lib.fileCaching import FileCache

coloradoWaterService = suds.client.Client('http://www.dwr.state.co.us/SMS_WebService/ColoradoWaterSMS.asmx?WSDL')
_districts = None

def getDistricts():
    global _districts
    cache = FileCache('ColoradoWater', 'Districts')
    
    if _districts is None:
        _districts = cache.loads(True, hours=24)
        
    if _districts is None:
        dists = coloradoWaterService.service.GetWaterDistricts()
        districts = []
        for district in dists.WaterDistrict:
            districts.append(WaterDistrict(response=district))
        _districts = districts
        
        cache.dumps(_districts, True)
        
    return _districts

def getDistrict(div, wd):
    wd = int(wd)
    div = int(div)
    for district in getDistricts():
        if district.wdID == wd and district.divID == div:
            return district
        
    return None

#def getStations():
#    response = coloradoWaterService.service.GetSMSTransmittingStations()
#    stations = []
#    for station in response.Station:
#        stations.append(Station(response=station))
#        
#    return stations
    

def utmToLatLng(zone, easting, northing, northernHemisphere=True):
    """
    Got code from http://stackoverflow.com/questions/343865/how-to-convert-from-utm-to-latlng-in-python-or-javascript
    """
    if not northernHemisphere:
        northing = 10000000 - northing

    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996

    arc = northing / k0
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

    ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

    ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

    cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    cc = 151 * math.pow(ei, 3) / 96
    cd = 1097 * math.pow(ei, 4) / 512
    phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

    n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

    r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
    fact1 = n0 * math.tan(phi1) / r0

    _a1 = 500000 - easting
    dd0 = _a1 / (n0 * k0)
    fact2 = dd0 * dd0 / 2

    t0 = math.pow(math.tan(phi1), 2)
    Q0 = e1sq * math.pow(math.cos(phi1), 2)
    fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

    fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

    lof1 = _a1 / (n0 * k0)
    lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
    lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
    _a3 = _a2 * 180 / math.pi

    latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

    if not northernHemisphere:
        latitude = -latitude

    longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

    return (latitude, longitude)
        
        
    
class WaterDistrict(object):
    def __init__(self, response=None):
        if response:
            self.wdID = int(response.wd)
            self.divID = int(response.div)
            self.name = response.waterDistrictName
        else:
            raise Exception, "Cannot create Water District without a SOAP Response, or WDID & Div ID"
        
        self.stations = None
        
    def __getstate__(self):
        dic = self.__dict__.copy()
        dic['stations'] = None
        return dic
            
    
    def getStations(self):
        cache = FileCache('ColoradoWater', 'Stations-'+str(self.divID)+"-"+str(self.wdID))
        if self.stations is None:
            self.stations = cache.loads(True, hours=24)
            if self.stations is not None:
                #Set Correct Ref to self
                for station in self.stations:
                    station.waterDist = self
            
        if self.stations is None:
            self.stations = []
            response = coloradoWaterService.service.GetSMSTransmittingStations(self.divID, self.wdID)
            self.stations = []
            try:
                for station in response.Station:
                    self.stations.append(Station(response=station, waterDist=self))
            except AttributeError, e:
                #This tends to be no stations for a district
                pass
                
            cache.dumps(self.stations, True)
            
        return self.stations
        
        
class Station(object):
    def __init__(self, response=None, wd=None, div=None, abbrev=None, waterDist=None):
        if wd and div and abbrev and not response:
            response = coloradoWaterService.service.GetSMSTransmittingStations(div, wd, abbrev).Station[0]
            waterDist = getDistrict(div, wd)
            
        if response:
            if waterDist is None:
                waterDist = getDistrict(response.div, response.wd)
                
            self.waterDist = waterDist
            self.name = response.stationName
            self.abbrev = response.abbrev
            self.dataProvider = response.DataProvider
            self.dataProviderAbbrev = response.DataProviderAbbrev
            self.utm_x = float(response.UTM_x)
            self.utm_y = float(response.UTM_y)
        else:
            raise Exception, "Cannot create Station without a SOAP Response, or WDID & Div ID & Station Abbrev"
        
        self.currentConditions = None
        
    def __getstate__(self):
        dic = self.__dict__.copy()
        dic['currentConditions'] = None
        dic['waterDist'] = None
        return dic
        
    def getLatLong(self):
        #Assuming UTM Zone 13 as it appears to not be documented and 13 covers most of Colorado
        return utmToLatLng(13, self.utm_x, self.utm_y)
    
    def getCurrentConditions(self):
        cache = FileCache('ColoradoWater', 'StationCurrentConditions-'+str(self.waterDist.divID)+"-"+str(self.waterDist.wdID)+"-"+self.abbrev)
        if self.currentConditions is None:
            self.currentConditions = cache.loads(True, hours=2)
            
        if self.currentConditions is None:
            self.currentConditions = StationConditions(self.waterDist.divID, self.waterDist.wdID, self.abbrev)
            cache.dumps(self.currentConditions, True)
            
        return self.currentConditions
    
class StationConditions(object):
    def __init__(self, div, wd, abbrev):
        #Discharge in 3ft/s
        self.discharge = 0
        #Air Temp in F
        self.airTemp = 0
        #Gage Height in FT
        self.gageHeight = 0
        
        response = coloradoWaterService.service.GetSMSCurrentConditions(div, wd, abbrev)
        try:
            for condition in response.CurrentCondition:
                if condition.variable == "DISCHRG":
                    self.discharge = float(condition.amount)
                elif condition.variable == "DISCHRG1" and self.discharge == 0:
                    self.discharge = float(condition.amount)
                elif condition.variable == "GAGE_HT":
                    self.gageHeight = float(condition.amount)
                elif condition.variable == "GAGE_HT1" and self.gageHeight == 0:
                    self.gageHeight = float(condition.amount)
                elif condition.variable == "AIRTEMP":
                    self.airTemp = float(condition.amount)
        except:
            pass
    