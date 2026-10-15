# C++ starting point:
# #include <vector>
#
# std::vector<std::vector<int>> transpose(const std::vector<std::vector<int>>& matrix) {
#     if (matrix.empty() || matrix[0].empty()) {
#         return {};
#     }
#     int rows = matrix.size();
#     int cols = matrix[0].size();
#     std::vector<std::vector<int>> result(cols, std::vector<int>(rows));
#     for (int i = 0; i < rows; ++i) {
#         for (int j = 0; j < cols; ++j) {
#             result[j][i] = matrix[i][j];
#         }
#     }
#     return result;
# }


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Chuyển vị ma trận 2D từ thuật toán C++.

    Điểm khác biệt chính so với bản C++:
    1. C++ cần khai báo kiểu tường minh `std::vector<std::vector<int>>` và cấp phát
       trước bộ nhớ `vector<vector<int>>(cols, vector<int>(rows))`. Trong Python,
       ma trận được biểu diễn bằng list lồng nhau và khởi tạo bằng list comprehension
       `[[0] * rows for _ in range(cols)]`.
    2. C++ lấy kích thước qua `.size()` và kiểm tra rỗng bằng `.empty()`, còn Python
       dùng hàm `len()` và kiểm tra truthiness (`if not matrix or not matrix[0]`).
    3. C++ cần truyền tham chiếu hằng (`const &`) để tránh sao chép tốn bộ nhớ;
       Python tự động truyền đối tượng qua object reference.
    """
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    result: list[list[int]] = [[0] * rows for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]

    return result
