from fastapi import APIRouter, UploadFile, File
from api.models.schemas import QueryRequest
from hashlib import md5
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from application.rag_pipeline import RAGPipeline, FAQPipeline
from dotenv import load_dotenv
from application.process_file import process_file
from domain.indexing.chunking import TextChunker
from domain.embedder import Embedder
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


@router.post("/chat-faq")
async def chat_faq(request: QueryRequest):
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
            faqqer = FAQPipeline()
            async for chunk in faqqer.process(user_message):
                yield str(chunk)
        except Exception as e:
            yield f"Lỗi khi xử lý yêu cầu: {str(e)}"

    return StreamingResponse(generate(), media_type="text/plain")


indexer = ChromaDBIndexer(collection_name="langchain")


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

    for chunk in doc_chunked:
        print(chunk, end="\n\n\n")

    if not doc_chunked:
        raise HTTPException(
            status_code=400, detail="Không tìm thấy nội dung hợp lệ sau khi chia nhỏ."
        )

    ids = [md5(text.encode()).hexdigest() for text in doc_chunked]

    embedder = Embedder()
    text_embedded = embedder.embed_text(doc_chunked)

    indexer.add_texts(doc_chunked, text_embedded, ids)

    return JSONResponse(
        content={"status": "success", "message": "Tải file thành công!"}
    )


@router.delete("/delete-collection/")
async def delete_collection():
    try:
        indexer.client.delete_collection("langchain")
        return {"message": "Collection langchain đã được xóa thành công."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi khi xóa collection: {str(e)}")
