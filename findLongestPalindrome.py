#!/usr/bin/python
#
class Solution(object):
	def longestPalindrome(self, s):
		total_len = len(s)
		left_index, right_index = 0, 0
		for i, c in enumerate(s):
			if i == 0:
				continue
			l, r = i - 1, i + 1
			while(l >= 0 and s[l] == c):
				l -= 1
			while(r < total_len and s[r] == c):
				r += 1
			k = min(l + 1, total_len - r)
			j = 0
			if k == 0:
				if r+j-1 - (l-j+1) > right_index - left_index:
					right_index, left_index = r+j-1, l-j+1
			else:
				for j in xrange(k):
					if s[l-j] != s[r+j]:
						if r+j-1 - (l-j+1) > right_index - left_index:
							right_index, left_index = r+j-1, l-j+1
						break
				else:				
					if r+j - (l-j) > right_index - left_index:
						right_index, left_index = r+j, l-j
		print left_index, right_index
		return s[left_index:right_index+1]

obj = Solution()
print obj.longestPalindrome("cbbd")

