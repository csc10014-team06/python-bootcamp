# W1-4: Bubble sort translated from C++ to Python.
#
# Original C++:
# void bubbleSort(std::vector<int>& a) {
#     int n = (int)a.size();
#     for (int i = 0; i < n - 1; i++) {
#         bool swapped = false;
#         for (int j = 0; j < n - 1 - i; j++) {
#             if (a[j] > a[j + 1]) {
#                 std::swap(a[j], a[j + 1]);
#                 swapped = true;
#             }
#         }
#         if (!swapped) break;
#     }
# }


def bubble_sort(a: list[int]) -> list[int]:
    """Sort a in place with bubble sort and return it.

    Differences from the C++ version:
    - Swapping uses tuple unpacking: a[j], a[j + 1] = a[j + 1], a[j],
      so no std::swap or temporary variable is needed.
    - A Python list knows its own length (len(a)), no size cast needed.
    - It returns the list, while the C++ version returns void.
    """
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a
