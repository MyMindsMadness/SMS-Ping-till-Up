import requests
import os
from dotenv import load_dotenv
from ping3 import ping
import time

load_dotenv('venv/.env')
# apikey = os.getenv('API_KEY')

apikey= input("Enter your TextBelt API key: ")
host = input("Enter the host to ping: ")
hostname = input("Enter the hostname ID: ")
required_pings = int(input("Enter the number of successful pings required to declare the host UP: "))
mobile_number = os.getenv('MOBILE_NUMBER')

def wait_till_up(host, required_pings):
    successful_pings = 0
    try:
        while True:
            rtt = ping(host, timeout=1.0, unit='ms')
            if rtt is not None:
                successful_pings += 1
                print (f'current successful ping count: {successful_pings}')
                if successful_pings >= required_pings:
                    message = f"Host {hostname} : Is declared UP!"
                    sms_notification(apikey, message, mobile_number)
                    return True
            else:
                if successful_pings > 0:
                    print ("host is not stable resetting counter")
                else:
                    print ('host is currently down')
                successful_pings = 0
            time.sleep(1)
    except Exception as e:
        print(f"Error occurred: {e}")
    return False

def sms_notification(apikey, message, mobile_number):
    resp = requests.post('https://textbelt.com/text', {
        'phone': mobile_number,
        'message': message,
        'key': apikey
    })
    print(resp.json())
    return resp.json()

wait_till_up(host, required_pings)
