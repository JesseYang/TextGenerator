wrong_set = set()
for i in range(10000):
    f = open('output/{}.txt'.format(i))
    line = f.readlines()[0]
    print(line)
print(wrong_set)
import os
for i in wrong_set:
    os.remove('output/{}.txt'.format(i))
    os.remove('output/{}.png'.format(i))
