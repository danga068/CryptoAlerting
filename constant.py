Group_A = ["BTC"]
Group_B = ["ETH", "XRP", "ADA"]
Group_C = ["DOGE"]

currencies = Group_A + Group_B + Group_C

rules = {
    "day": {
        "Group_A": {
            "1_min": 0.70,
            "3_min": 0.90,
            "5_min": 1.2,
            "10_min": 1.5,
            "15_min": 1.8,
            "30_min": 2.1,
            "60_min": 3.0
        },
        "Group_B": {
            "1_min": 1.0,
            "3_min": 1.3,
            "5_min": 1.5,
            "10_min": 1.7,
            "15_min": 1.9,
            "30_min": 2.7,
            "60_min": 3.5
        },
        "Group_C": {
            "1_min": 2,
            "3_min": 2.6,
            "5_min": 3,
            "10_min": 4,
            "15_min": 5,
            "30_min": 7,
            "60_min": 9
        }
    },
    "night": {
        "Group_A": {
            "1_min": 2.0,
            "3_min": 2.8,
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
            "1_min": 6,
            "3_min": 7,
            "5_min": 8,
            "10_min": 10,
            "15_min": 12,
            "30_min": 14,
            "60_min": 17
        }
    },
    "hot": {
        "1_min": 5,
        "3_min": 5,
        "5_min": 5,
        "10_min": 3,
        "15_min": 5,
        "30_min": 5,
        "60_min": 5
    }
}

integration_key = "39e531e5217a470dc0c6956f05d9728e"
# redis_host = "34.82.159.43"
redis_host = "127.0.0.1"
redis_pass = "dangaiit068"
redis_db = 0

try:
    from local_settings import *
except ImportError as error:
    pass

