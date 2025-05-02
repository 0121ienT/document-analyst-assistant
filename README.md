# AI Assistant for Project Document Analysis

## Giới thiệu
Dự án **AI Assistant for Project Document Analysis** là một trợ lý AI được thiết kế để hỗ trợ các Business Analyst (BA) trong việc phân tích tài liệu dự án. Trợ lý này sử dụng công nghệ xử lý ngôn ngữ tự nhiên (NLP) để tự động trích xuất thông tin quan trọng, phân loại yêu cầu, và cung cấp gợi ý dựa trên các tài liệu như SRS (Software Requirement Specification), BRD (Business Requirement Document), hoặc các ghi chú dự án, phân tích các nguồn tài liệu khác nhau.

Mục tiêu của dự án là giảm thiểu thời gian xử lý thủ công, tăng độ chính xác trong phân tích yêu cầu, và hỗ trợ BA trong việc lập kế hoạch và giao tiếp với các bên liên quan.

## Tính năng chính
- **Trích xuất thông tin**: Tự động nhận diện và rút trích các yêu cầu chính từ tài liệu (ví dụ: functional/non-functional requirements).
- **Phân loại yêu cầu**: Gắn nhãn yêu cầu theo loại (business rules, user needs, technical constraints).
- **Gợi ý cải tiến**: Đưa ra đề xuất tối ưu hóa yêu cầu dựa trên dữ liệu lịch sử hoặc best practices.
- **Hỗ trợ đa định dạng**: Xử lý tài liệu dạng PDF, Word, và văn bản được thêm vào.

## Công nghệ sử dụng
- **Ngôn ngữ lập trình**: Python
- **Thư viện NLP**: SpaCy, NLTK, Transformers (Hugging Face)
- **Machine Learning**: Các mô hình học sâu để phân tích văn bản (BERT, RoBERTa)
- **Lưu trữ dữ liệu**: SQLite (dự kiến mở rộng sang PostgreSQL)

## Cài đặt
1. **Clone repository**:
   ```bash
   git clone https://github.com/username/ai-assistant-for-ba.git
   cd ai-assistant-for-ba
   ```
2. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Chạy ứng dụng**:
   ```bash
   python main.py
   ```

## Cách sử dụng
- Đưa tài liệu dự án vào thư mục `input/`.
- Chạy script phân tích:
  ```bash
  python analyze.py --file input/document.pdf
  ```
- Kết quả sẽ được lưu trong `output/results.json`.

## Đóng góp
Chúng tôi hoan nghênh mọi đóng góp! Để tham gia:
1. Fork repository.
2. Tạo branch mới (`git checkout -b feature/ten-tinh-nang`).
3. Commit thay đổi (`git commit -m "Mô tả thay đổi"`).
4. Push lên branch (`git push origin feature/ten-tinh-nang`).
5. Tạo Pull Request.

## Tác giả
- **Nguyễn Thị Vân** - Business Analyst & AI Enthusiast
  - Email: [nghean2501@gmail.com](mailto:nghean2501@gmail.com)
  - GitHub: [vannnguyen](https://github.com/vannnguyen)

## Giấy phép
Dự án được phát hành dưới [MIT License](LICENSE).
