# String matching: Find if a string is a substring of another. Note that a mismatch of one character
# should be ignored. A mismatch is either an extra character ('dog' matches ‘xxxdoogyyyy'), a
# missing char ('dog' matches ‘xxxxdgyyyy') or a different character ('dog' matches ‘xxxdigyyyy').
# Write code in a language of your choice.

def find_fuzzy_string(s, p, k=1):
	"""
	s - string to search in
	p - pattern we're looking for
	k - number of allowed mismatches
	"""

	n = len(s)
	m = len(p)

	dp = [[0 for j in xrange(m+1)] for i in xrange(n+1)]

	for i in xrange(n+1):
		dp[i][0] = i+1

	for j in xrange(m+1):
		dp[0][j] = j+1

	for i in xrange(1, n+1):
		for j in xrange(1, m+1):
			if s[i-1] != p[j-1]:
				dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
			else:
				dp[i][j] = dp[i-1][j-1]

	for c in xrange(1, n+1):
		allowed_mistakes = k
		i = c
		j = m
		while i > 0 and j > 0 and allowed_mistakes >= 0:
			if s[i-1] != p[j-1]:
				allowed_mistakes -= 1
				if dp[i][j]-1 == dp[i][j-1]:
					j -= 1
				elif dp[i][j]-1 == dp[i-1][j]:
					i -= 1
				else:
					i -= 1
					j -= 1
			else:
				i -= 1
				j -= 1

		if allowed_mistakes >= 0 and j <= allowed_mistakes:
			yield (i, c)



