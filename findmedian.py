
class Solution(object):
	def findMedianOfSortedArrays(self, nums1, nums2):
		n1, n2 = len(nums1), len(nums2)
		if n1 > n2:
			n1, n2 = n2, n1
			nums1, nums2 = nums2, nums1
		if n1 == 0:
			if n2 == 0:
				return
			mid, rem = divmod(n2, 2)
			if rem == 1:
				return nums2[mid]
			else:
				return (nums2[mid-1]+nums2[mid])/2.0
			
		mid, rem = divmod(n1 + n2, 2)
		i, j = n1/2, mid-n1/2
		
		for _ in xrange(n1+1):
			if i != 0 and nums1[i-1] > nums2[j]:
				i -= 1
				j += 1
			elif i != n1 and nums2[j-1] > nums1[i]:
				i += 1
				j -= 1
			else:
				if i == n1:
					min_right = nums2[j]
				elif j == n2:
					min_right = nums1[i]
				else:
					min_right = min(nums1[i], nums2[j])
				print min_right
				if rem == 1:
					return min_right
				
				if i == 0:
					max_left = nums2[j-1]
				elif j == 0:
					max_left = nums1[i-1]
				else:
					max_left = max(nums1[i-1], nums2[j-1])
				print max_left
				return (max_left + min_right)/2.0
