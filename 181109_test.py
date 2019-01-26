language = 'english'
abbre = 'en'
test = """ %(a)s %(a)s "%(b)s" """
print(test % {'a': language, 'b': abbre})
test2 = """{} {}"""
test2.format("hello", "world")
test3 = """{} {}""".format("hello", "world")
