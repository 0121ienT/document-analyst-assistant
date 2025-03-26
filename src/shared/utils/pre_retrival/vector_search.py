import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from chromadb import PersistentClient
from typing import Optional, List

# Kết nối ChromaDB
client = PersistentClient(path="./chroma_db")

# Khởi tạo vectorstore với embedding từ OpenAI
vectorstore = Chroma(client=client, collection_name="langchain", embedding_function=OpenAIEmbeddings())

def remove_duplicates(docs: List[str]) -> List[str]:
    """
    Loại bỏ các kết quả trùng lặp dựa trên nội dung tài liệu.

    Args:
        docs (List[str]): Danh sách các tài liệu thu được từ truy vấn.

    Returns:
        List[str]: Danh sách tài liệu sau khi đã loại bỏ trùng lặp.
    """
    unique_docs = list(set(docs))  # Dùng set để loại bỏ trùng lặp, sau đó chuyển về danh sách
    return unique_docs

def vector_search(query: str) -> Optional[str]:
    """
    Tìm kiếm thông tin trong cơ sở dữ liệu vector sử dụng ChromaDB và lọc kết quả trùng lặp.

    Args:
        query (str): Câu truy vấn cần tìm kiếm.

    Returns:
        Optional[str]: Nội dung của các tài liệu liên quan nhất (đã loại bỏ trùng lặp)
                       hoặc thông báo nếu không tìm thấy kết quả.
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # Lấy 5 tài liệu liên quan nhất
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found in vector database."

    # Lọc bỏ tài liệu trùng lặp
    unique_contents = remove_duplicates([doc.page_content for doc in docs])

    # Trả về nội dung tài liệu đã loại bỏ trùng lặp
    return "\n\n".join(unique_contents)

