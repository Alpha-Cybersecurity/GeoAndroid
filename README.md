# GeoAndroid
Position Android Phone without GPS signal


Actualmente exiten otros metodos de posicionar un terminal sin la necesidad de utilizar la señal GPS. A traves de Google Maps Geolocation API ubicaremos un dispositivo.

https://developers.google.com/maps/documentation/geolocation/intro?hl=es-419

## Getting started
Existe 4 maneras de posicionar un dispositivo sin necesidad de GPS
* #### Direccion IP 
  La manera mas basica de geoposicionar un dispositivo. 

        datos = {
           "considerIp": "true"
        }


* #### Wifi 
    Utilizacion de tecnica wardriving. Muchos personas usan dispositivos GPS para determinar la ubicación de los hotspots hallados y registrarla en un sitio web

        datos = {
            "considerIp": "false",
            "wifiAccessPoints": [
                {
                    "macAddress": "xx-xx-xx-xx-xx-xx",
                    "signalStrength": -48,
                    "signalToNoiseRatio": 0
                },
                {
                    "macAddress": "xx-xx-xx-xx-xx-x1",
                    "signalStrength": -49,
                    "signalToNoiseRatio": 0
                }
            ]
        }
        
* #### Cell ID Tower
    CDMA, LTE y GSM principales sistemas de radio utilizados en los teléfonos celulares. Para mas informacion     https://es.wikipedia.org/wiki/MCC/MNC

          
          
            
        datos = {
            "considerIp": "false",
            "cellTowers": [
                {
                    "cellId": CID,
                    "locationAreaCode": LAC,
                    "mobileCountryCode": MCC,
                    "mobileNetworkCode": MNC
                }
            ]
        }

* #### Share location browser

![Image of location](https://github.com/NoSuitsSecurity/GeoAndroid/blob/master/images/location.png)


## Installation

#### Obtención de Database
Existen diferentes bases de datos de donde podemos sacar informacion.
* Herrevad: This database contains the WiFi connections history of preinstalled Google apps in Android OS devices. It can be WIFI connections of Google Play, Google Maps, Youtube, etc    
    
    /data/com.google.android.gms/databases/herrevad  
    
* Wigle:

* Astro:  


#### Instalar programa
Para instalar el porgrama ejecutaremos los sigueintes comandos

    git clone https://github.com/NoSuitsSecurity/GeoAndroid.git    
    cd GeoAndroid
    pip install -r requirements.txt  

Change API Credential:
Necesitas crear una Clave de API de Google para poder utilizar esta utilidad. Para crear una clave visite esta pagina https://developers.google.com/maps/documentation/geolocation/intro?hl=es-419

Una vez obtenia la clave, cambia:
    
    GeoForensic.py
    9   YOUR_API_KEY = " "
    
    templates/index.html
    7   'mapsApiKey': ' '
    
  

Uso:
    
    usage: python3 GeoForensic.py [options]

    Example with long option names
    
    optional arguments:
      -h,  --help              Show this help message and exit
      -db, --db_path DB_PATH   Path of sqlite
      -t,  --type TYPE         herrevad or wigle
 
Ejemplo:
    
    python3 GeoForensic.pyimport -db /home/usuario/Documents/herrevad.db -t herrevad



#### Ejemplo
En la carpeta _**Template**_ encontraremos el archivo __*.html__ en funcion de las opciones que hayamos escogido. 

![Image of output](https://github.com/NoSuitsSecurity/GeoAndroid/blob/master/images/output.png)

