Group_A = ["XRP"]
Group_B = ["ETH", "TRX"]
Group_C = []

currencies = Group_A + Group_B + Group_C

rules = {
    "day": {
        "Group_A": {
            "1_min": 0.60,
            "3_min": 0.85,
            "5_min": 1.0,
            "10_min": 1.5,
            "15_min": 1.5,
            "30_min": 2.0,
            "60_min": 3.0
        },
        "Group_B": {
            "1_min": 0.80,
            "3_min": 1.0,
            "5_min": 1.2,
            "10_min": 1.5,
            "15_min": 1.8,
            "30_min": 2.2,
            "60_min": 3.0
        },
        "Group_C": {
            "1_min": 4,
            "3_min": 5,
            "5_min": 6.5,
            "10_min": 8,
            "15_min": 10,
            "30_min": 12,
            "60_min": 15
        }
    },
    "night": {
        "Group_A": {
            "1_min": 2,
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
            "1_min": 4,
            "3_min": 5,
            "5_min": 6.5,
            "10_min": 8,
            "15_min": 10,
            "30_min": 12,
            "60_min": 15
        }
    }
}


integration_key = "5168fd3d64294735bb04e51a7e65734c"
redis_host = "159.89.167.82"
redis_pass = "dangaiit068"
