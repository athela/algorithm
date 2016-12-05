#!/usr/bin/python
#convert rows of zigzag string to one line string
'''
n=numRows
D=2n-2    1                           2n-1                         4n-3
D=        2                     2n-2  2n                    4n-4   4n-2
D=        3               2n-3        2n+1              4n-5       .
D=        .           .               .               .            .
D=        .       n+2                 .           3n               .
D=        n-1 n+1                     3n-3    3n-1                 5n-5
D=2n-2    n                           3n-2                         5n-4
'''
class Solution(object):
	def convert(self, s, numRows):
		"""
		:type s: str
		:type numRows: int
		:rtype: str
		"""
		lenth = len(s)
		if numRows <= 1 or lenth <= 2:
			return s
		
		ret = ""	
		for i in xrange(1, numRows+1):		
			if i == 1 or i == numRows:
				k = i
				while(1 <= k <= lenth):				
					ret += s[k-1]
					k = 2*numRows-2 + k
			else:
				if 1 <= i <= lenth:
					ret += s[i-1]
				k2 = 2*numRows-2+i
				k1 = k2 - 2*(i-1)
				while(1 <= k1 <= lenth and 1 <= k2 <= lenth):
					ret += s[k1-1]
					ret += s[k2-1]
					k2 = 2*numRows-2 + k2
					k1 = k2 - 2*(i-1)
				if 1 <= k1 <= lenth:
					ret += s[k1-1]
				if 1 <= k2 <= lenth:
					ret += s[k2-1]
		return ret   


c = Solution()
print c.convert("ABC", 3)