import json
import time
import pypd
import pytz
import datetime
import requests

from redis_config import Redis
from crypro_alert import trigger_alert_script


class CryptoCompareDataWarehouse:
    def __init__(self):
        self.last_notification = 0
        self.redis_client = Redis().connection()
        self.time_zone = pytz.timezone('Asia/Kolkata')
        self.url = "https://min-api.cryptocompare.com/data/top/totalvolfull?limit=100&tsym=USD"

    def is_valid_notification(self):
       return (int(time.time()) - self.last_notification) > 60 # 10 Mins

    def mobile_notification(self, message):
        self.last_notification = int(time.time())
        pypd.EventV2.create(data={
            'routing_key': self.redis_client.get("integration_key"),
            'event_action': 'trigger',
            'payload': {
                'summary': message,
                'severity': 'error',
                'source': 'pypd bot',
            }
        })

    def data_pull(self):

        index = self.redis_client.get("last_index") or 0
        index = int(index) + 1

        while True:
            try:
                response = requests.get(self.url)
                coin_info_list = json.loads(response.text).get("Data", [])

                payload = {}
                for coin_info in coin_info_list:
                    price = coin_info.get("RAW").get("USD").get("PRICE")
                    symbol = coin_info.get("RAW").get("USD").get("FROMSYMBOL")
                    payload[symbol] = price
                payload["datetime"] = str(datetime.datetime.now(self.time_zone).strftime('%Y-%m-%d %H:%M:%S'))

                self.redis_client.set("last_index", str(index))
                self.redis_client.setex(index, 12*3600, str(payload))

                print ("Processing Index: ", index)
                index += 1
                trigger_alert_script()
                time.sleep(60)
            except Exception as err:
                if self.is_valid_notification():
                    self.mobile_notification(str(err))

try:
    crypto_compare = CryptoCompareDataWarehouse()
    crypto_compare.data_pull()
except Exception as err:
    crypto_compare.mobile_notification("Service Stopped: " + str(err))

