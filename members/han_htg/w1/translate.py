# This is the C++ version:
# void insertionSort(vector<int>& nums) {
#     for (int i = 1; i < nums.size(); i++) {
#         int key = nums[i];
#         int j = i - 1;

#         while (j >= 0 && nums[j] > key) {
#             nums[j + 1] = nums[j];
#             j--;
#         }
#         nums[j + 1] = key;
#     }
# }

def insertion_sort(nums: list[int]):
    """
    Sorts a list of integers in-place in ascending order using Insertion Sort.

    Difference from C++:
    In C++, the parameter must be explicitly declared as a reference (`vector<int>& nums`)
    to modify the original array in-place. In Python, lists are mutable objects passed by
    object reference automatically, so mutating `nums` modifies the caller's list in-place
    without any special reference syntax. 

    Additionally, Python uses 'range(1, len(nums))', 
    'and', and 'j -= 1' instead of C-style 'for' loops, '&&', and 'j--').
    """
    
    for i in range(1, len(nums)):
        key = nums[i]
        j = i - 1

        while j >= 0 and nums[j] > key:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key

    return nums
