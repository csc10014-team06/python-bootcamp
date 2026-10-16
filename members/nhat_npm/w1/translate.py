# Starting Point
# int binary_search(const std::vector<int>& a, int key) {
#   int lo = 0, hi = (int)a.size() - 1;
#   while (lo <= hi) {
#       int mid = lo + (hi - lo) / 2;
#       if (a[mid] == key) return mid;
#       if (a[mid] < key) lo = mid + 1; else hi = mid - 1;
#   }
# return -1;
# }


def binary_search(a: list[int], key: int) -> int:
    """Find key in a sorted list; unlike C++, Python uses len(a) for its size."""
    lo = 0
    hi = len(a) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if a[mid] == key:
            return mid
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1

