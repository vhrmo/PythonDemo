sample = [1, ["another", "list"], ("a", "tuple")]
print sample

mylist = ["List item 1", 2, 3.14, 5, 'Item X']
print mylist

mylist[0] = "List item 1 again"  # We're changing the item.
print mylist

mylist[-1] = 'Item Y'  # Here, we refer to the last item.
print mylist

mydict = {"Key 1": "Value 1", 2: 3, "pi": 3.14}
print mydict

mydict["pi"] = 3.15  # This is how you change dictionary values.
print mydict

mytuple = (1, 2, 3)
print mytuple

myfunction = len
print(myfunction(mylist))

print(mylist[:])
print(mylist[0:2])
print(mylist[:-1])
print(mylist[1:])

# Adding a third parameter, "step" will have Python step in
# N item increments, rather than 1.
# E.g., this will return the first item, then go to the third and
# return that (so, items 0 and 2 in 0-indexing).
print(mylist[::2])
