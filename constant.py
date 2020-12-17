Group_A = []
Group_B = []
Group_C = ["BTC", "XRP", "ETH"]

currencies = Group_A + Group_B + Group_C

rules = {
    "day": {
        "Group_A": {
            "1_min": 0.70,
            "3_min": 0.90,
            "5_min": 1.2,
            "10_min": 1.5,
            "15_min": 1.7,
            "30_min": 2.0,
            "60_min": 3.0
        },
        "Group_B": {
            "1_min": 0.80,
            "3_min": 1.0,
            "5_min": 1.2,
            "10_min": 1.6,
            "15_min": 1.9,
            "30_min": 2.2,
            "60_min": 3.0
        },
        "Group_C": {
            "1_min": 1,
            "3_min": 1.5,
            "5_min": 2,
            "10_min": 3.5,
            "15_min": 6,
            "30_min": 7,
            "60_min": 9
        }
    },
    "night": {
        "Group_A": {
            "1_min": 2.0,
            "3_min": 2.7,
            "5_min": 3.0,
            "10_min": 3.3,
            "15_min": 3.5,
            "30_min": 4.0,
            "60_min": 4.5
        },
        "Group_B": {
            "1_min": 2.5,
            "3_min": 2.9,
            "5_min": 3.2,
            "10_min": 3.5,
            "15_min": 3.7,
            "30_min": 4.0,
            "60_min": 4.5
        },
        "Group_C": {
            "1_min": 2.5,
            "3_min": 3.5,
            "5_min": 4.5,
            "10_min": 6,
            "15_min": 8,
            "30_min": 9,
            "60_min": 10
        }
    }
}


integration_key = "c92adfb7701f4b1b822c91557392fd35"
# redis_host = "34.82.159.43"
redis_host = "127.0.0.1"
redis_pass = "dangaiit068"
redis_db = 0

try:
    from local_settings import *
except ImportError as error:
    pass

