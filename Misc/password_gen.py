#python

import sys
import random
import string

def gen_password(sym1, sym2):
	return sym1 + gen_random_number(3) +  sym2 + gen_random_number(3) + gen_random_word(4)

def gen_random_number(l):
	number = ''
	for i in range(l):
		number += random.choice(string.digits)
	return number

def gen_random_word(l):
	word = ''
	capi = random.choice([0, 1, 2, 3])
	for i in range(l):
		if capi == i:
			word += random.choice(string.ascii_uppercase)
		else:
			word += random.choice(string.ascii_lowercase)
	return word

if __name__ == '__main__':
	#for i in range(len(sys.argv)):
	#	print(i, ') ', sys.argv[i])

	if len(sys.argv) != 3:
		print('Must provide exactly two command line arguments')
		exit(1)

	print(gen_password(sys.argv[1], sys.argv[2]))

	#syml = symbols.split()
	#print(gen_password(syml[0], syml[1]))
