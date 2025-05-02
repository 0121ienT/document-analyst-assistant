from fastapi import FastAPI
from src.api.routers import router  # Import router từ file chứa API endpoints
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()
app = FastAPI()

# Đăng ký router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
