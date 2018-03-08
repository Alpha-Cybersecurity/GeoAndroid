import argparse
import os
import requests
import sqlite3


#Constant

YOUR_API_KEY = "YOUR API KEY HERE"
URL = "https://www.googleapis.com/geolocation/v1/geolocate?key="

WIGLE_WIFI_QUERY = "select lastlat, lastlon, bssid from network group by bssid"
HERREAVAD_WIFI_QUERY = "select bssid from local_reports group by bssid"
HERREAVAD_CELL_QUERY  = "select rowkey from lru_table group by rowkey"



def SQLite(Path, Query):
    '''
    This fuction return de result of the query of SQLite
        :param Path: The path of db
        :param Query: Query to extract information
    :return: Result of query
    '''

    result = []

    conn = sqlite3.connect(Path)
    cur = conn.cursor()
    rows = cur.execute(Query).fetchall()

    for row in rows:
        result.append(list(row))

    return result



def GoogleGeolocationAPI(Data, Name):
    '''
    This fuction interacts with Google API, get precision and acurrency of data
        :param Data: json for request to Google API
        :param Name: Mac for represent in Google Maps
    :return:  Array with latitude, longitude and name
    '''

    response = requests.post(URL+YOUR_API_KEY, json=Data)

    if response.status_code == 200:
        lat = response.json()['location']['lat']
        long = response.json()['location']['lng']

        return [lat, long, Name]




def DireccionIP():
    '''
    First method for get position of any device. Get lat, long and acurrency of IP
    :return:Array with latitude, longitude and name
    '''

    datos = {
        "considerIp": "true"
    }
    return datos


def AccesPointWifi(Bssid):
    '''
    Second method for get position of any device. Get lat, long and acurrency  with
    Wardriving thecnique.
        :param Bssid: Unique name to identificate a Wifi
    :return:Array with latitude, longitude and name
    '''

    geolocation = []
    geolocation.append(['Lat', 'Long', 'Name'])

    for mac in Bssid:
        if mac is not None:
            datos = {
                "wifiAccessPoints": [
                    {
                        "macAddress": "%s" % mac,
                    }
                ]
            }
            geolocation.append(GoogleGeolocationAPI(datos, mac))

    return geolocation


def AccesPointWifiTriangulation(Bssid):
    '''
    Second method for get position of any device. Is better because use technical triangulation.
        :param Bssid: Unique name to identificate a Wifi
    :return:Array with latitude, longitude and name
    '''

    """
    geolocation = []
    geolocation.append(['Lat', 'Long', 'Name'])

    for mac in Bssid:
        datos = {
            "considerIp": "false",
            "wifiAccessPoints": [
                {
                    "macAddress": "%s" % Bssid[1],
                    "signalStrength": -48,
                    "signalToNoiseRatio": 0
                },
                {
                    "macAddress": "%s" % Bssid[2],
                    "signalStrength": -49,
                    "signalToNoiseRatio": 0
                }
            ]
        }
        geolocation.append(GoogleGeolocationAPI(datos, mac))

    return geolocation
    """


def TowerCell(CellTower):
    '''
    Third method for get position of any device. Get lat, long and acurrency  with GSM. LTE or CDMA log's.
        :param CellTower: Recive CellID, Location area, Mobile Country Code and mobile Network
    :return:Array with latitude, longitude and name

    The log's recived "gsm:214:03:9150:2401"
        type = gsm
        mobileCountryCode (MCC) = 214
        mobileNetworkCode (MNC) = 03
        locationAreaCode  (LAC) = 9150
        cellId            (CID) = 2401

    https://es.wikipedia.org/wiki/MCC/MNC
    '''

    geolocation = []
    geolocation.append(['Lat', 'Long', 'Name'])

    for gsm in CellTower:
        if gsm.startswith('gsm') or gsm.startswith('lte') or gsm.startswith('cdma'):
            gsm = gsm.split(":")
            datos = {
                "considerIp": "false",
                "cellTowers": [
                    {
                        "cellId": gsm[4],
                        "locationAreaCode": gsm[3],
                        "mobileCountryCode": gsm[1],
                        "mobileNetworkCode": gsm[2]
                    }
                ]
            }

            geolocation.append(GoogleGeolocationAPI(datos, gsm[4]))

    return geolocation



def outputHtml(Name, ArrayData):
    '''
    Print the GeoData in html geo chart like a map.
        :param Name: Name of output file
        :param ArrayData: Array with latitude, longitude and name
    :return: the output is a html
    '''

    file = open('templates/index.html', 'r')
    text = file.read()
    geoWifi = text.replace('{{ array }}', ArrayData)
    file.close()


    file = open("templates/%s.html"%Name, "w")
    file.write(geoWifi)
    file.close()




if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='GeoForensic', description='Example with long option names', usage='python3 GeoForensic.py [options]')
    parser.add_argument('--db_path','-db', help="Path of sqlite")
    parser.add_argument('--type','-t', help="herrevad or wigle")

    args = parser.parse_args()
    dbPath = args.db_path

    if os.path.exists(dbPath):
        if args.type == "herrevad":
            LocationBssid = AccesPointWifi(SQLite(dbPath, HERREAVAD_WIFI_QUERY))
            outputHtml("HERREAVAD_WIFI",str(LocationBssid))

            CellTower = TowerCell(SQLite(dbPath, HERREAVAD_CELL_QUERY))
            outputHtml("HERREAVAD_CELL",str(CellTower))

        elif args.type == "wigle":
            LocationBssid = SQLite(dbPath, WIGLE_WIFI_QUERY)
            LocationBssid.insert(0, ['Lat', 'Long', 'Name'])
            outputHtml("WIGLE_WIFI", str(LocationBssid))

        else:
            print("Please, use a correct type")



    else:
        print("Doesn't exit path")

