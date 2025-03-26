# def detect_question_type(question: str) -> str:
#     """
#     Xác định loại câu hỏi dựa trên từ khóa.
    
#     Trả về:
#     - "qa" nếu câu hỏi có từ khóa tìm kiếm thông tin
#     - "chatbot" nếu là câu giao tiếp thông thường
#     """
#     qa_keywords = ["là gì", "ai", "khi nào", "tại sao", "ở đâu", "cách", "làm thế nào"]
    
#     if any(keyword in question.lower() for keyword in qa_keywords):
#         return "qa"
#     return "chatbot"

# # Test
# print(detect_question_type("Albert Einstein là ai?"))  # Kết quả: "qa"
# print(detect_question_type("Bạn có khỏe không?"))       # Kết quả: "chatbot"

# Cách 1 : viết hàm đơn giản để phân loại câu querry 
def detect_question_type(question: str) -> str:
    """
    Xác định loại câu hỏi dựa trên từ khóa.
    
    Trả về:
    - "qa" nếu câu hỏi có từ khóa tìm kiếm thông tin
    - "chatbot" nếu là câu giao tiếp thông thường
    """
    qa_keywords = ["là gì", "ai", "khi nào", "tại sao", "ở đâu", "cách", "làm thế nào"]
    
    if any(keyword in question.lower() for keyword in qa_keywords):
        return "qa"
    return "chatbot"

# # Test
# print(detect_question_type("Albert Einstein là ai?"))  # Kết quả: "qa"
# print(detect_question_type("Bạn có khỏe không?"))       # Kết quả: "chatbot"
