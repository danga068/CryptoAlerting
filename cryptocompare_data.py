import json
import time
import requests

from redis import Redis


class CryptoCompareDataWarehouse:
    def __init__(self):
        self.redis_client = Redis().connection()
        self.url = "https://min-api.cryptocompare.com/data/top/totalvolfull?limit=50&tsym=USD"

    def data_pull(self):
        x = 1
        while True and x:
            try:
                response = requests.get(self.url)
                coin_info_list = json.loads(response.text).get("Data", [])

                for coin_info in coin_info_list:

                import pdb; pdb.set_trace()

                x = 0
                time.sleep(60)
            except Exception as e:
                print ("Error ", e)

try:
    crypto_compare = CryptoCompareDataWarehouse()
    crypto_compare.data_pull()
except Exception as err:
    PagerDuty().callPagerDuty("Alerting System Down!!!" + str(err))


