class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        leng = 1
        res = 1
        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]:
                leng += 1
                res = max(res, leng)
            else:
                leng = 1
        return res