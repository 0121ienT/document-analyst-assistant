from fastapi import APIRouter ,UploadFile , File
# from src.services.query_handler import QueryHandler
from api.models.schemas import QueryRequest, QueryResponse
from hashlib import md5
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from application.rag_pipeline import RAGPipeline
router = APIRouter()


@router.post("/chat")
async def chat(request: QueryRequest):
    user_message = request.text

    if not isinstance(user_message, str):
        raise HTTPException(status_code=400, detail="Lỗi: user_message phải là một chuỗi (str)")

    if not user_message.strip():  # Kiểm tra rỗng
        raise HTTPException(status_code=400, detail="Lỗi: user_message không được để trống")

    async def generate():
        try:
            ragger = RAGPipeline()
            async for chunk in ragger.process(user_message):  # Dùng async for
                yield str(chunk)
        except Exception as e:
            yield f"Lỗi khi xử lý yêu cầu: {str(e)}"

    return StreamingResponse(generate(), media_type="text/plain")


    




