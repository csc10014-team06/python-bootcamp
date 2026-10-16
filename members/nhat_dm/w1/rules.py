def can_register_thesis(credits: int, gpa: float) -> bool:
    """
    Kiểm tra sinh viên có đủ điều kiện đăng ký khóa luận tốt nghiệp hay không.
    Điều kiện: credits >= 120 và gpa >= 2.0.
    """
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """
    Trả về danh sách lý do chưa đủ điều kiện làm khóa luận tốt nghiệp.
    """
    reasons = []
    
    if credits < 120:
        needed_credits = 120 - credits
        reasons.append(f"need {needed_credits} more credits")
        
    if gpa < 2.0:
        needed_gpa = round(2.0 - gpa, 2)
        reasons.append(f"need {needed_gpa} more GPA")
        
    return reasons