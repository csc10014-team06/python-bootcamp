def primes_up_to(n: int) -> list[int]:
    """    
    Điểm khác biệt so với C++:
    Trong C++, ta thường cấp phát một mảng `bool is_prime[MAXN]` tĩnh hoặc dùng 
    `std::vector<bool>` (vốn được tối ưu hóa bit ngầm định nhưng có thể chậm). 
    Trong Python, mảng boolean được khởi tạo cực kỳ ngắn gọn và hiệu quả thông qua 
    phép nhân list: `[True] * (n + 1)`. Thêm vào đó, thay vì viết vòng lặp for 
    truyền thống `for(int j = i*i; j <= n; j += i)` để đánh dấu bội số, Python 
    sử dụng tham số `step` tích hợp sẵn trong hàm `range(i * i, n + 1, i)`.
    """
    if n < 2:
        return []
    
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
                
    return [p for p, prime in enumerate(is_prime) if prime]