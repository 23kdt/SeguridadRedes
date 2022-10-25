import string
import time
import sys
import os
import itertools


ascii = string.ascii_lowercase
def make_dict():
    
    fichero = open('wordlist.txt','w')

    for comb in itertools.product(ascii,repeat=6):
        it = (''.join(comb))
        print(it)
        fichero.write(it+'\n')

if __name__ == '__main__':
    make_dict()