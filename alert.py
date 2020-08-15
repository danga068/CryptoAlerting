from constant import *
import json
import time
import requests
import pypd
import datetime

from datetime import datetime

class PagerDuty(object):
    def __init__(self):
        self.last_pager = 900000000
        self.integration_key = "3d32bae209b8447295cc86a51f264576"

    def is_valid_pager(self):
       return (int(time.time()) - self.last_pager) > 60*30 # 10 Mins

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


class CryptoCompare:
    def __init__(self):
        self.last_pager = 900000000
        self.is_first_call = False

        self.sleep_time_range = [1, 9]
        self.url = "https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym=USD&limit=61&aggregate=1"

        self.is_call = True
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
                message = "{currency} price change by {price_diff_percent} in last {key_time}, From: {last_price} to: {current_price}".format(currency=currency, price_diff_percent=price_diff_percent, key_time=key_time, last_price=last_price, current_price=current_price)
                return True, message

        return False, ""


    def check_alert(self):
        while True:
            try:
                if PagerDuty().is_valid_pager():
                    for currency in currencies:
                        url = self.url.format(currency)
                        response = requests.get(url)

                        try:
                            crypto_prices = json.loads(response.text)
                            price_history = crypto_prices.get("Data", [])

                            is_pager, message = self.send_alert_on_pagerduty(currency, price_history)

                            if is_pager and not self.is_first_call:
                                self.last_pager = int(time.time())
                                PagerDuty().callPagerDuty(message)
                                print (message)
                            else:
                                print ("{}: No Pager here !!!!".format(currency))
                        except Exception as e:
                                print ("Api error : ", response.text)
                    print ("\n\n")
                    time.sleep(30)
                    self.is_first_call = False
            except Exception as e:
                print ("Error ", e)

try:
    crypto_compare = CryptoCompare()
    crypto_compare.check_alert()
except Exception as err:
    PagerDuty().callPagerDuty("Alerting System Down!!!" + str(err))
