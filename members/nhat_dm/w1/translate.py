# // C++ starting point
# int binary_search(const std::vector<int>& a, int key) {
#     int lo = 0, hi = (int)a.size() - 1;
#     while (lo <= hi) {
#         int mid = lo + (hi - lo) / 2;
#         if (a[mid] == key) return mid;
#         if (a[mid] < key) lo = mid + 1; else hi = mid - 1;
#     }
#     return -1;
# }

def binary_search(a: list[int], key: int) -> int:
    """
    Perform a binary search on a sorted list of integers.
    Returns the index of the key if found, otherwise returns -1.

    Key differences from the C++ implementation:
    1. In C++, `mid = lo + (hi - lo) / 2` is used to prevent integer overflow.
       In Python, integers have arbitrary precision and cannot overflow, 
       so writing `(lo + hi) // 2` is safe and standard.
    2. Python uses the `//` operator for integer division (the `/` operator always returns a float).
    3. Variable types do not need explicit type declarations (`lo`, `hi`, `mid`).
    """
    lo = 0
    hi = len(a) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        
        if a[mid] == key:
            return mid
        elif a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1