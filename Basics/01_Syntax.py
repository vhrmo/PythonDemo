
myvar = 3
print myvar

myvar += 2
print myvar

if myvar == 5:
    print 'myvar is equal to five'
else:
    print 'myvar is NOT equal to five'

"""This is a multiline comment.
The following lines concatenate the two strings."""

mystring = "Hello"
mystring += " world."
print(mystring)

# This swaps the variables in one line(!).
myvar, mystring = mystring, myvar

print "myvar:", myvar
print "mystring:", mystring
