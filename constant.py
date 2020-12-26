Group_A = []
Group_B = ["BTC"]
Group_C = ["XRP"]

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
            "1_min": 1.6,
            "3_min": 2,
            "5_min": 4,
            "10_min": 6.5,
            "15_min": 8,
            "30_min": 10,
            "60_min": 15
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
            "1_min": 6,
            "3_min": 7,
            "5_min": 9,
            "10_min": 11,
            "15_min": 13,
            "30_min": 14,
            "60_min": 17
        }
    }
}


integration_key = "984c1ae796da486a9507d60c3fd98f82"
# redis_host = "34.82.159.43"
redis_host = "127.0.0.1"
redis_pass = "dangaiit068"
redis_db = 0

try:
    from local_settings import *
except ImportError as error:
    pass

