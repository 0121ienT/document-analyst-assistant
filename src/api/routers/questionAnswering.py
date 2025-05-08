from fastapi import APIRouter, UploadFile, File

# from src.services.query_handler import QueryHandler
from api.models.schemas import QueryRequest
from hashlib import md5
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from application.rag_pipeline import RAGPipeline
from dotenv import load_dotenv
from src.application.process_file import process_file
from src.domain.indexing.chunking import TextChunker
from src.domain.embedder import Embedder
from infra.chromaIndexer import ChromaDBIndexer
from fastapi.responses import JSONResponse

load_dotenv()

router = APIRouter()


@router.post("/chat")
async def chat(request: QueryRequest):
    user_message = request.text
    print("User Message:", user_message)
    if not isinstance(user_message, str):
        raise HTTPException(
            status_code=400, detail="Lỗi: user_message phải là một chuỗi (str)"
        )

    if not user_message.strip():
        raise HTTPException(
            status_code=400, detail="Lỗi: user_message không được để trống"
        )

    async def generate():
        try:
            ragger = RAGPipeline()
            async for chunk in ragger.process(user_message):
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
    docs = process_file(file)

    chunker = TextChunker(method="semantic")
    doc_chunked = chunker.chunk(docs)

    if not doc_chunked:
        raise HTTPException(
            status_code=400, detail="Không tìm thấy nội dung hợp lệ sau khi chia nhỏ."
        )

    ids = [md5(text.encode()).hexdigest() for text in doc_chunked]

    embedder = Embedder()
    text_embedded = embedder.embed_text(doc_chunked)

    indexer = ChromaDBIndexer(collection_name="langchain")
    indexer.add_texts(doc_chunked, text_embedded, ids)

    return JSONResponse(
        content={"status": "success", "message": "Tải file thành công!"}
    )
