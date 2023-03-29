import time

import web
import discord_alert
import sensors
import collect

def message_lcd():
    print("lcd !!!")
    message, pseudo = collect.get_last_message_from_db()
    sensors.print_on_lcd('{}\nFrom : {}'.format(message,pseudo), 'message')	
    
    while sensors.button.state != True:
        pass

def main():
    nb_alert = {"sound":0,"temp":0,"co":0}
    while True:
       
        temp, sound, percentage_co, number_msg = collect.get_value_from_sensors()
        collect.new_value_in_db(temp, sound, percentage_co, number_msg)

        sensors.print_on_lcd('Temp:{}°C  \ndB:{} CO:{}ppm'.format(round(temp,2),sound,percentage_co), 'normal')
        print(temp,sound,percentage_co)
        if sound > 600 :
            nb_alert["sound"] += 1
            sensors.print_on_lcd('Alert : Sound \nis too high !', 'error')
            while sensors.button.state != True:
                sensors.sound_alert(1)
            sensors.sound_alert(0)

        if percentage_co > 700:
            nb_alert["co"] += 1
            sensors.print_on_lcd('Alert : CO \nis too high !', 'error')
            while sensors.button.state != True:
                sensors.sound_alert(1)
            sensors.sound_alert(0)
        
        if temp > 30:
            nb_alert["temp"] += 1
            sensors.print_on_lcd('Alert : Temp \nis too high !', 'error')
            while sensors.button.state != True:
                sensors.sound_alert(1)
            sensors.sound_alert(0)
        
        if nb_alert["sound"] >= 3:
            discord_alert.raise_alert("high sound")
            nb_alert["sound"] = 0
        
        if nb_alert["co"] >= 3:
            discord_alert.raise_alert("carbon monoxide")
            nb_alert["co"] = 0
        
        if nb_alert["temp"] >= 3:
            discord_alert.raise_alert("temperature")
            nb_alert["temp"] = 0
        
        time.sleep(0.5)


if __name__ == '__main__':
    main()
