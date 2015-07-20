# coding=utf-8
# https://de.wikipedia.org/wiki/Baeza-Yates-Gonnet-Algorithmus
import math

def bin(value):
	"""
	Utility function to see binary representation of Number
	without two-complement notation
	"""
	bits = 32  # bits to show
	if value < 0:
		value = ( 1<<bits ) + value
	formatstring = '{:0%ib}' % bits
	return formatstring.format(value)

def rightmost_zero(n):
	"""
	Return index of rightmost zero
	"""
	return math.log(n&(-n), 2) + 1


def get_start_index(dp, i, j, m):
	# We don't know how many inserts or deletes were made in order
	# to match substring of s to p. But we know that we made at most i
	# inserts or deletes. If we did deletes they must be somewhere in substring,
	# so substring could be of length m + [number of deletes].
	# If we did inserts, then substring length could be m - [number of inserts].
	# If we did both then substring length is m + [number of deletes] - [number of inserts]
	print i, j, m
	if i == 0:
		return max(j-m+1, 0)

	if rightmost_zero(dp[i][j] | dp[i-1][j-1]) == rightmost_zero(dp[i-1][j-1]):  # if last step was delete
		print 'del'
		return get_start_index(dp, i-1, j-1, m)
	elif rightmost_zero(dp[i][j] | dp[i-1][j]) == rightmost_zero(dp[i-1][j]):  # last step was insert
		print 'ins'
		return get_start_index(dp, i-1, j, m)
	elif rightmost_zero(dp[i][j] | (dp[i-1][j-1]<<1)) == rightmost_zero(dp[i-1][j-1]<<1):  # last step was delete
		print 'repl'
		return get_start_index(dp, i-1, j-1, m)
	else:
		print 'match'
		return get_start_index(dp, i-1, j, m)

def agrep(s, p, k):
	"""
	Find match of p in s with at most k errors. Error could be extra
	character, absence of a character or incorrect character in string s.

	Current implementation is limited to:
	- string s should contain only a-z characters
	- pattern p should be no longer than 32 characters
	"""
	n = len(s)
	m = len(p)

	if m > 32:
		return

	# ~0 = 11111111111111111111111111111111 in binary form
	alphabet = dict()
	for c in xrange(ord('a'), ord('z')+1):
		alphabet[chr(c)] = ~0

	# Imagine we have pattern `aba`, for each character we
	# will create a mask with 0's on position equal to its
	# position in pattern p. For example, `a` mask will be 11111111111111111111111111111010
	# and `b` 11111111111111111111111111111101
	i = 0
	for c in p:
		alphabet[c] &= ~(1<<i)
		# print c, bin(alphabet[c]),
		i += 1


	# ~1 = 11111111111111111111111111111110
	# the leftmost 0 will indicate our progress of matching p to s, once
	# it reach position of len(p) - we found the match.
	# dp[i][j] indicates current state of our search of p in s[:j]
	# with exactly i errors
	dp = [[~1 for j in xrange(n+1)] for i in xrange(k+1)]

	for i in xrange(k+1):
		for j in xrange(1, n+1):
			c = s[j-1]
			mask = alphabet[c]
			dp[i][j] = (dp[i][j-1] | mask)<<1

			# i == 0 is exact match step, i.e. no errors
			if i > 0:
				# Pretend we never were on step j (i.e. we never saw character j-1 in s),
				# for this we just need to use the state we were before (with one mistake less)
				delete = dp[i-1][j-1]
				# If we would like to insert another character after s[j-1] which would match
				# appropriate character in p, whis would mean we take state for current character
				# but with one less mistake dp[i-1][j] and shift it to the right, since we need
				# to update the state and move to next character
				insert = dp[i-1][j]<<1
				# Replacing character s[j-1] means, we take previous step and just shift it to left
				# i.e. pretend match did happen and we move to next character
				replace = dp[i-1][j-1]<<1

				# Now we combine all possible scenarios with exact match and move to next step with
				# assembled/merged state of the search
				dp[i][j] &= insert & delete & replace

			if (dp[i][j]&(1<<m)) == 0:
				start = get_start_index(dp, i, j, m)
				end = j
				yield (start, end, i)


s = 'xxxadayyy'
for i,j,k in agrep(s, 'abc', 2):
	print s[:i], '-', s[i:j], '-', s[j:]


# find_fuzzy_string('xxxxdgyyyy', 'dog')
# find_fuzzy_string('xxxdoogyyyy', 'dog')
# find_fuzzy_string('xxxdigyyyy', 'dog')
