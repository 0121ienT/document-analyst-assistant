from fastapi import APIRouter ,UploadFile , File 
# from src.services.query_handler import QueryHandler
from src.api.models.schemas import QueryRequest, QueryResponse
from hashlib import md5
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from src.application.rag_pipeline import RAGPipeline
from dotenv import load_dotenv
import os
from src.application.process_file import process_file
from src.domain.indexing.chunking import TextChunker 
from src.domain.embedder import Embedder
from infra.chromaIndexer import ChromaDBIndexer
from fastapi.responses import JSONResponse

# Load biến môi trường từ file .env

load_dotenv()

router = APIRouter()


@router.post("/chat")
async def chat(request: QueryRequest):
    user_message = request.text
    print("User Message:",user_message)
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


@router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    """
    API nhận file tải lên và xử lý nội dung.

    Args:
        file (UploadFile): File tải lên từ người dùng.

    Returns:
        dict: Kết quả xử lý file.
    """
    # Bước 1: Load nội dung tài liệu
    docs = process_file(file)  # Lấy văn bản từ file

    # Bước 2: Chia nhỏ tài liệu (Chunking)
    chunker = TextChunker(method='semantic')
    doc_chunked = chunker.chunk(docs)  # List[str]

    if not doc_chunked:
        raise HTTPException(status_code=400, detail="Không tìm thấy nội dung hợp lệ sau khi chia nhỏ.")

    # Bước 3: Tạo IDs cho từng đoạn văn bản
    ids = [md5(text.encode()).hexdigest() for text in doc_chunked]

    # Bước 4: Chuyển văn bản thành vector embeddings
    embedder = Embedder()
    text_embedded = embedder.embed_text(doc_chunked)  # List[list[float]]

    # Bước 5: Lưu vào ChromaDB
    indexer = ChromaDBIndexer(collection_name="langchain")
    indexer.add_texts(doc_chunked, text_embedded, ids)

    return JSONResponse(content={"status": "success", "message": "Tải file thành công!"})

    




