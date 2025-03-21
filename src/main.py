from fastapi import FastAPI
from src.api.routers import  router  # Import router từ file chứa API endpoints

app = FastAPI()

# Đăng ký router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
