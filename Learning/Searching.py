
def binary_search(nums, target):
  i, j = 0, len(nums) - 1
  while i <= j:
    m = (i + j) // 2  #CALCULATE THE MIDDLE INDEX
    if nums[m] < target:
      i = m + 1  #MOVE THE LFET INDEX UP
    else nums[m] > target:  
      j = m - 1
    else:  #MOVE THE RIGHT INDEX DOWN
      return m  #TARGET FOUND, RETURN THE INDEX
  return -1 #TARGET NOT FOUND
