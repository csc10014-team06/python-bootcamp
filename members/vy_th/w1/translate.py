# vy_th — C++ starting point
# long long gcd(long long a, long long b) {
#     while (b != 0) {
#         long long r = a % b;
#         a = b;
#         b = r;
#     }
#     return a;
# }


def gcd(a: int, b: int) -> int:
    """
    Compute the GCD using the Euclidean algorithm.

    In Python, we do not need to explicitly declare variable types, such as long long r in C++. Python's int can represent arbitrarily large integers without overflow, unlike C++'s int or long long.

    Additionally, Python supports simultaneous assignment, allowing us to update multiple variables without using a temporary variable like r = a % b.
    """
    while b != 0:
        a, b = b, a % b

    return a
