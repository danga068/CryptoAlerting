import json
import time
import requests
import pypd
import datetime

from datetime import datetime

from constant import *
from redis_config import Redis


class PagerDuty(object):
    def __init__(self):
        self.last_pager = 900000000
        self.integration_key = "5168fd3d64294735bb04e51a7e65734c"

    def is_valid_pager(self):
       return (int(time.time()) - self.last_pager) > 60*3 # 10 Mins

    def callPagerDuty(self, message):
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

        self.sleep_time_range = [1, 9]
        if self.sleep_time_range[0] <= datetime.now().hour <= self.sleep_time_range[1]:
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
        if self.sleep_time_range[0] <= datetime.now().hour <= self.sleep_time_range[1]:
            shift_type = "night"
        else:
            shift_type = "day"
        return shift_type

    def send_alert_on_pagerduty(self, currency, price_history):
        last_index = len(price_history) - 1
        current_price = price_history[last_index].get("close")

        shift_type = self.get_shift()
        group = self.get_currency_group(currency)
        if not group:
            return None

        alert_rules_dict = rules[shift_type][group]

        for key_time in alert_rules_dict:
            change_percent = alert_rules_dict[key_time]

            time_min = int(key_time.split('_')[0])
            last_price = price_history[last_index-time_min].get("close")
            price_diff = current_price - last_price

            price_diff_percent = round(((price_diff * 100) / last_price), 2)

            if abs(price_diff_percent) >= change_percent:
                message = "{currency} price change by {price_diff_percent}% in last {key_time}, From: {last_price} to: {current_price}".format(currency=currency, price_diff_percent=price_diff_percent, key_time=key_time, last_price=last_price, current_price=current_price)
                return True, message

        return False, ""


    def check_alert(self):
        try:
            shift_type = self.get_shift()

            for currency in currencies:
                group = self.get_currency_group(currency)
                print (currency, " -- ", group, " -- " , shift_type)

            # 
            # alert_rules_dict = rules[shift_type][group]

            # for key_time in alert_rules_dict:
            #     change_percent = alert_rules_dict[key_time]

            #     time_min = key_time.split('_')[0]

            #     self.redis_client.get("integration_key")

            #     time.sleep(100)
            #     self.is_first_call = False
        except Exception as e:
            print ("Error ", e)


def trigger_alert_script():
    try:
        CryptoAlert().check_alert()
    except Exception as err:
        PagerDuty().callPagerDuty("Alerting System Down!!!" + str(err))


trigger_alert_script()