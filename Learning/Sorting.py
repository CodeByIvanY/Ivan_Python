"""Sort the array using the quicksort algorithm."""
def partition(nums, left, right):
  """PARTITION THE ARRY AROUND A PIVOT."""
  i, j = left, right
  while i < j:
    while i < j and nums[j] >= nums[left]:
      j -=1
    while i <j and nums[i] <= nums[left]:
      i +=1
    nums[i], nums[j] = nums[j], nums[i]
  nums[i], nums[left] = nums[left], nums[i]
  return i

def quick_sort(nums, left, right):
  if left >= right:
    return
  pivot = partition(nums, left, right)  #Partition the array
  quick_sort(nums, left, pivot - 1)  # Recursively sort the left subarray
  quick_sort(nums, pivot + 1, right) # Recursively sort the right subarray
