data = {
    "name": "Malcolm",
    "occupation": "pilot",
    "age": 34,
    "city": "Toronto"
}


def update_age(newAge=100):
    global data
    data["age"] = newAge


def get_fields(data, fields=["name", "age"]):
    return [val for key, val in data.items() if key in fields]


def get_name_and_age(data):
    return data["name"], data["age"]


update_age(120)

print get_fields(data)
print get_fields(data, ["city"])

name, age = get_name_and_age(data)
print "{} is {} years old".format(name, age)

