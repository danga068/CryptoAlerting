import ast
import json
import time
import requests
import pypd
import pytz

from datetime import datetime

from constant import *
from redis_config import Redis


class PagerDuty(object):
    def __init__(self):
        self.last_pager = 0
        self.integration_key = "ca1d7de318cb4290a2a8d00fb981d9ce"

    def callPagerDuty(self, message, is_error=False):
        print ("Calling Pager ...", message)
        pypd.EventV2.create(data={
            'routing_key': self.integration_key,
            'event_action': 'trigger',
            'payload': {
                'summary': message,
                'severity': 'error',
                'source': 'pypd bot',
            }
        })


class CryptoAlert:
    def __init__(self):
        self.last_pager = 900000000
        self.is_first_call = False

        self.redis_client = Redis().connection()
        self.time_zone = pytz.timezone('Asia/Kolkata')
        self.current_datetime_ist = datetime.now(self.time_zone)

        self.sleep_time_range = [1, 9]
        if self.sleep_time_range[0] <= self.current_datetime_ist.hour <= self.sleep_time_range[1]:
            shift_type = "night"
        else:
            shift_type = "day"

    def getBitBnsPrices(self):
        bitbns_response = requests.get("https://bitbns.com/order/getTickerWithVolume/")
        bitbns_prices = json.loads(bitbns_response.text)

        message = " Bitbns -- "
        message += "BTC: " + str(bitbns_prices.get("BTC").get("yes_price")) + ", "
        message += "XRP: " + str(bitbns_prices.get("XRP").get("yes_price")) + ", "
        message += "LTC: " + str(bitbns_prices.get("LTC").get("yes_price")) + ", "
        message += "ETH: " + str(bitbns_prices.get("ETH").get("yes_price"))

        return message

    def get_currency_group(self, currency):
        if currency in Group_A:
            return "Group_A"
        elif currency in Group_B:
            return "Group_B"
        elif currency in Group_C:
            return "Group_C"
        return None

    def get_shift(self):
        self.sleep_time_range = [1, 9]
        if self.sleep_time_range[0] <= self.current_datetime_ist.hour <= self.sleep_time_range[1]:
            shift_type = "night"
        else:
            shift_type = "day"
        return shift_type

    def check_alert(self):
        try:
            shift_type = self.get_shift()

            last_index = self.redis_client.get("last_index")

            current_price = ast.literal_eval(self.redis_client.get(int(last_index)).decode("utf-8"))
            last_1_min = ast.literal_eval(self.redis_client.get(int(last_index) - 1).decode("utf-8"))
            last_3_min = ast.literal_eval(self.redis_client.get(int(last_index) - 3).decode("utf-8"))
            last_5_min = ast.literal_eval(self.redis_client.get(int(last_index) - 5).decode("utf-8"))
            last_10_min = ast.literal_eval(self.redis_client.get(int(last_index) - 10).decode("utf-8"))
            last_15_min = ast.literal_eval(self.redis_client.get(int(last_index) - 15).decode("utf-8"))
            last_30_min = ast.literal_eval(self.redis_client.get(int(last_index) - 30).decode("utf-8"))
            last_60_min = ast.literal_eval(self.redis_client.get(int(last_index) - 60).decode("utf-8"))

            last_x_prices = [last_1_min, last_3_min, last_5_min, last_10_min, last_30_min, last_60_min]

            for currency in currencies:
                message = None
                group = self.get_currency_group(currency)
                # for last_x_price in last_x_prices:
                #     diff_x_min = (((current_price[currency] - last_x_price[0][currency]) * 100) / last_x_price[0][currency])

                diff_1_min = round((((current_price[currency] - last_1_min[currency]) * 100) / last_1_min[currency]), 2)
                diff_3_min = round((((current_price[currency] - last_3_min[currency]) * 100) / last_3_min[currency]), 2)
                diff_5_min = round((((current_price[currency] - last_5_min[currency]) * 100) / last_5_min[currency]), 2)
                diff_10_min = round((((current_price[currency] - last_10_min[currency]) * 100) / last_10_min[currency]), 2)
                diff_15_min = round((((current_price[currency] - last_15_min[currency]) * 100) / last_15_min[currency]), 2)
                diff_30_min = round((((current_price[currency] - last_30_min[currency]) * 100) / last_30_min[currency]), 2)
                diff_60_min = round((((current_price[currency] - last_60_min[currency]) * 100) / last_60_min[currency]), 2)

                if abs(diff_1_min) >= rules[shift_type][group]["1_min"] and not self.redis_client.get(currency+"_1_min"):
                    self.redis_client.setex(currency+"_1_min", 1*60+3, 1)
                    message = currency + " last 1 min change: " + str(diff_1_min) + " current price: " +  str(current_price[currency])

                elif abs(diff_3_min) >= rules[shift_type][group]["3_min"] and not self.redis_client.get(currency+"3_min"):
                    self.redis_client.setex(currency+"_3_min", 3*60+3, 1)
                    message = currency + " last 3 min change: " + str(diff_3_min) + " current price: " +  str(current_price[currency])

                elif abs(diff_5_min) >= rules[shift_type][group]["5_min"] and not self.redis_client.get(currency+"5_min"):
                    self.redis_client.setex(currency+"_5_min", 5*60+3, 1)
                    message = currency + " last 5 min change: " + str(diff_5_min) + " current price: " +  str(current_price[currency])

                elif abs(diff_10_min) >= rules[shift_type][group]["10_min"] and not self.redis_client.get(currency+"10_min"):
                    self.redis_client.setex(currency+"_10_min", 10*60+3, 1)
                    message = currency + " last 10 min change: " + str(diff_10_min) + " current price: " +  str(current_price[currency])

                elif abs(diff_15_min) >= rules[shift_type][group]["15_min"] and not self.redis_client.get(currency+"15_min"):
                    self.redis_client.setex(currency+"_15_min", 15*60+3, 1)
                    message = currency + " last 15 min change: " + str(diff_15_min) + " current price: " +  str(current_price[currency])

                elif abs(diff_30_min) >= rules[shift_type][group]["30_min"] and not self.redis_client.get(currency+"30_min"):
                    self.redis_client.setex(currency+"_30_min", 30*60+3, 1)
                    message = currency + " last 30 min change: " + str(diff_30_min) + " current price: " +  str(current_price[currency])

                elif abs(diff_60_min) >= rules[shift_type][group]["60_min"] and not self.redis_client.get(currency+"60_min"):
                    self.redis_client.setex(currency+"_60_min", 60*60+3, 1)
                    message = currency + " last 60 min change: " + str(diff_60_min) + " current price: " +  str(current_price[currency])
                if message:
                    print (self.current_datetime_ist, message, shift_type, group)
                    PagerDuty().callPagerDuty(message)
        except Exception as e:
            print ("Error ", e)
            PagerDuty().callPagerDuty("Alerting System Down!!!" + str(e), is_error=True)


def trigger_alert_script():
    CryptoAlert().check_alert()
