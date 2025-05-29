import random

prefixes = ["Jon", "Daen", "Tyr", "Ary", "Sers", "Khal", "Bri", "Rob", "St", "Cer"]
suffixes = ["ark", "arys", "ion", "a", "ei", "o", "enne", "ert", "an", "ei"]

def generate_name():
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    return prefix + suffix

for _ in range(10):
    print(generate_name())