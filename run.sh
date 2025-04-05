#!/bin/bash

# Chạy FastAPI backend trong background
echo "🔄 Đang khởi động FastAPI backend..."
python3 /Users/luongthaison/Documents/Third_years_student/Project/document-analyst-assistant/document-analyst-assistant/src/main.py &

# Lưu PID để sau có thể dừng lại nếu cần
BACKEND_PID=$!

# Chạy Chainlit frontend (giả sử là app.py sử dụng chainlit run)
echo "💬 Đang khởi động Chainlit frontend..."
chainlit run /Users/luongthaison/Documents/Third_years_student/Project/document-analyst-assistant/document-analyst-assistant/frontend/app.py

# Khi Chainlit kết thúc, cũng dừng FastAPI
echo "🛑 Dừng backend..."
kill $BACKEND_PID
