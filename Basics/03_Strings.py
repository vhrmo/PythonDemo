name = 'Vlado'

print "Name: %s \nNumber: %s \nString: %s\n" % (name, 3, 3 * "-")

print("This %(verb)s a %(noun)s.\n" % {"noun": "test", "verb": "is"})

print """This is
a multiline
string.\n"""

print "Hello, {}!\n".format(name)

print("The capital of {province} is {capital}".format(province="Ontario", capital="Toronto"))

data = {"province": "Alberta", "capital": "Edmonton"}
print("The capital of {province} is {capital}\n".format(**data))

# see https://pyformat.info/ for all the magic
for i in range(10):
    # print "{:>10}".format(10**i)
    # print "{0:>10}".format(10**i)  # in python 2.6 param index is mandatory
    # print "{num:>10}".format(num=10**i)
    # print "{num:>010}".format(num=10**i)
    print "{num:13.2f}".format(num=10**i+0.25)

