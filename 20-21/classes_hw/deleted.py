from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # numbers_dict = { nums[i] : i for i in range(len(nums))} # O(N) времени, O(N) памяти

        numbers_dict = {}

        for i in range(len(nums)):
            if target - nums[i] not in numbers_dict:
                numbers_dict[nums[i]] = i
            else:
                return numbers_dict[target - nums[i]], i

#         for i in numbers_dict: # O(N) времени
#             j = target - i
#             if j in numbers_dict and numbers_dict[i] != numbers_dict[j]: # O(1)
#                 return [numbers_dict[i], numbers_dict[j]]


# # сортировка O(N log N) +
# for i in range(len(nums)): # O(N^2)
#     for j in range(i + 1, len(nums)):
#         if nums[i] + nums[j] == target:
#             return [i, j]


# 4 10 -1 2 1000         12

# -1 2 4 10 1000        12