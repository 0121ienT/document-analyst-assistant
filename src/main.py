from fastapi import FastAPI
from api import router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Đăng ký router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
