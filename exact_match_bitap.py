# coding=utf-8

def grep(s, p):
	"""
	Find exact match of p in s
	http://en.wikipedia.org/wiki/Bitap_algorithm

	Current implementation is limited to:
	- string s should contain only a-z characters
	- pattern p should be no longer than 32 characters
	"""
	n = len(s)
	m = len(p)

	if m > 32:
		return

	alphabet = dict()
	for c in xrange(ord('a'), ord('z')+1):
		alphabet[chr(c)] = ~0

	i = 0
	for c in p:
		alphabet[c] &= ~(1<<i)
		i += 1

	result = ~1
	i = 0
	for c in s:
		mask = alphabet[c]
		result = (result | mask) << 1

		if (result&(1<<m)) == 0:
			yield (i-m+1, i+1)

		i += 1

