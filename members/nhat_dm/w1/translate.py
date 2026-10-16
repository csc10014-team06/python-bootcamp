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
    Thực hiện tìm kiếm nhị phân trên một danh sách số nguyên đã sắp xếp.
    Trả về vị trí index của key nếu tìm thấy, ngược lại trả về -1.

    Điểm khác biệt chính so với bản C++:
    1. Trong C++, việc tính `mid = lo + (hi - lo) / 2` được dùng để tránh hiện tượng tràn số nguyên (integer overflow). 
       Trong Python, kiểu số nguyên (int) có độ dài tùy biến và không bị tràn số, nên ta có thể viết trực tiếp `(lo + hi) // 2`.
    2. Python sử dụng toán tử chia lấy phần nguyên `//` thay vì `/` (toán tử `/` trong Python luôn trả về số thực float).
    3. Python không cần khai báo kiểu dữ liệu cho biến cục bộ (`lo`, `hi`, `mid`).
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