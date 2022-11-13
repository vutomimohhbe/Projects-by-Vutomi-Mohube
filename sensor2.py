from sense_emu import SenseHat
from datetime import datetime
import time
from influxdb import InfluxDBClient


####1. READ FROM SENSOR
sensor = SenseHat()
readings = {}

while True:
    sensor.clear()
    temp = round(sensor.get_temperature(),1)
    press = round(sensor.get_pressure(), 1)
    hum = round(sensor.get_humidity(),1)
    
    print(temp)
    print(press)
    print(hum)
    print("===============================")
       
#####2. STORE IN DB
    ##2a. connect to the DB
    dbHost = "localhost"
    dbPort = "8086"
    dbUser = "coadmin"
    dbPwd = "IOT2022"
    db = "IOT2022"
    try:
        dbClient = InfluxDBClient(dbHost, dbPort, dbUser, dbPwd, db)
    except:
        print("Something went wrong while trying to connect to the DB")
        
    dataBaseEntry = []
    readings['measurement'] = 'trucks'
    readings['tags'] = {'licenseNo':'A001'}
    readings['time'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    readings['fields'] = {
        'temperature': temp,
        'humidity': hum,
        'pressure': press}
    dataBaseEntry.append(readings)
        
    response = dbClient.write_points(dataBaseEntry)
    if response == True:
        print ("Saved Successfully")
    else:
        print("ERRRROOOOOOORRRRR!!!!")
    
    time.sleep(10)    

    