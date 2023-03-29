# Connexion to InfluxDB
#!/usr/bin/env python3

import datetime
from influxdb import InfluxDBClient
import sensors

# influx configuration
ifuser = "GrafanaUser"
ifpass = "GrafanaPassword"
ifdb   = "DatabaseName"
ifhost = "127.0.0.1"
ifport = 8086

# ---------------------------------------

def new_value_in_db(temp, sound, percentage_co, number_msg):
    time = datetime.datetime.utcnow()

    body = [
        {
            "measurement": "stats",
            "time": time,
            "fields": {
                "temperature": temp,
                "sound": sound,
                "percentage_co": percentage_co,
                "number_msg": number_msg,
            }
        }
    ]

    client = InfluxDBClient(ifhost, ifport, ifuser, ifpass, ifdb)
    client.write_points(body)

    return True


def new_message_in_db(message,pseudo):
    time = datetime.datetime.utcnow()

    body = [
        {
            "measurement": "messages",
            "time": time,
            "fields": {
                "message": message,
                "pseudo": pseudo,
            }
        }
    ]

    client = InfluxDBClient(ifhost, ifport, ifuser, ifpass, ifdb)
    client.write_points(body)

    return True


def get_number_msg_from_db():
    try:
        client = InfluxDBClient(ifhost, ifport, ifuser, ifpass, ifdb)
        result = client.query('select * from messages order by time desc limit 1;')
        points = result.get_points()
        for point in points:
            number_msg = point['number_msg']
        return number_msg
    except:
        return 0    

def get_value_from_sensors():
    temp = sensors.temperature() 
    sound = sensors.sound()
    percentage_co = sensors.gas_main()
    #number_msg = get_number_msg_from_db()

    return temp, sound, percentage_co, 0


def get_last_value_from_db():
    client = InfluxDBClient(ifhost, ifport, ifuser, ifpass, ifdb)
    result = client.query('select * from "stats" order by time desc limit 1;')
    points = result.get_points()
    temp = 0
    sound = 0
    percentage_co = 0
    number_msg = 0
    for point in points:
        temp = point['temperature']
        sound = point['sound']
        percentage_co = point['percentage_co']
        number_msg = point['number_msg']
    return temp, sound, percentage_co, number_msg
 
 
def get_last_message_from_db():
    try:
        client = InfluxDBClient(ifhost, ifport, ifuser, ifpass, ifdb)
        result = client.query('select * from messages order by time desc limit 1;')
        points = result.get_points()
        print(points)
        message = ""
        pseudo = ""
        for point in points:
            message = point['message']
            pseudo = point['pseudo']
    except:
        message =  "No message"
        pseudo = "None"
    return message, pseudo
