print(range(10))

for number in range(10):
    print number

data = [
    {"name": "John", "surname": "Doe"},
    {"name": "Vlado", "surname": "Hrmo"},
    {"name": "John", "surname": "Dicks"},
    {"name": "Frank", "surname": "Mannon"}
]

for item in data:
    if 1==1:
    # if item["name"] == "John":
    # if item["name"] not in ("John", "Frank"):
        print "{name:>8} {surname}".format(**item)

data = {
    "name": "Malcolm",
    "occupation": "pilot",
    "age": 34,
    "city": "Toronto"
}

print
for key in data:
    print "{:>10}:{}".format(key, data[key])

print
for key, value in data.items():
    print "{:>10}:{}".format(key, value)
