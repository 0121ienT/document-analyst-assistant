Dưới đây là phiên bản tiếng Anh của file `README.md` giới thiệu về dự án trợ lý AI hỗ trợ phân tích tài liệu dự án cho Business Analyst (BA). Nội dung ngắn gọn, chuyên nghiệp và theo chuẩn Markdown.

---

# AI Assistant for Project Document Analysis

## Overview
The **AI Assistant for Project Document Analysis** is an AI-powered tool designed to assist Business Analysts (BAs) in analyzing project documents. Leveraging natural language processing (NLP), it automatically extracts key information, categorizes requirements, and provides actionable insights from documents such as SRS (Software Requirement Specification), BRD (Business Requirement Document), or project notes.

The goal is to minimize manual processing time, enhance requirement analysis accuracy, and support BAs in planning and stakeholder communication.

## Key Features
- **Information Extraction**: Automatically identifies and extracts core requirements (e.g., functional/non-functional requirements).
- **Requirement Classification**: Labels requirements by type (business rules, user needs, technical constraints).
- **Improvement Suggestions**: Offers optimization recommendations based on historical data or best practices.
- **Multi-Format Support**: Processes PDF, Word, and plain text documents.

## Technologies Used
- **Programming Language**: Python
- **NLP Libraries**: SpaCy, NLTK, Transformers (Hugging Face)
- **Machine Learning**: Deep learning models for text analysis (BERT, RoBERTa)
- **Data Storage**: SQLite (with plans to scale to PostgreSQL)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/ai-assistant-for-ba.git
   cd ai-assistant-for-ba
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage
- Place project documents in the `input/` directory.
- Run the analysis script:
  ```bash
  python analyze.py --file input/document.pdf
  ```
- Results will be saved in `output/results.json`.

## Contributing
We welcome contributions! To get involved:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/feature-name`).
3. Commit your changes (`git commit -m "Describe changes"`).
4. Push to the branch (`git push origin feature/feature-name`).
5. Submit a Pull Request.

## Author
- **Van Nguyen Thi** - Business Analyst & AI Enthusiast
  - Email: [nguyenvank58t2@gmail.com](mailto:nguyenvank58t2@gmail.com)
  - GitHub: [vannnguyen](https://github.com/vannnguyen)

## License
This project is licensed under the [MIT License](LICENSE).
