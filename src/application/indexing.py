import chromadb
from langchain_openai import OpenAIEmbeddings
from typing import List
import uuid


class ChromaDBIndexer:
    """
    Lớp hỗ trợ lưu trữ và truy vấn embedding vào ChromaDB.
    """

    def __init__(
        self, collection_name: str, model_name: str = "text-embedding-ada-002"
    ):
        """
        Khởi tạo kết nối với ChromaDB và model embedding.

        Args:
            collection_name (str): Tên collection trong ChromaDB.
            model_name (str, optional): Model embedding của OpenAI. Mặc định là "text-embedding-ada-002".
        """
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_model = OpenAIEmbeddings(model=model_name)
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_texts(
        self, texts: List[str], embeddings: List[List[float]], ids: List[str]
    ):
        """
        Thêm văn bản và embedding vào ChromaDB. Nếu ID bị trùng, tự động tạo ID mới.

        Args:
            texts (List[str]): Danh sách văn bản.
            embeddings (List[List[float]]): Danh sách vector embeddings tương ứng.
            ids (List[str]): Danh sách ID tương ứng với văn bản.
        """
        if len(texts) != len(embeddings) or len(texts) != len(ids):
            raise ValueError("Số lượng texts, embeddings và ids phải bằng nhau!")

        existing_ids = set(self.collection.get()["ids"])

        new_ids = []
        for original_id in ids:
            new_id = original_id
            while new_id in existing_ids:
                new_id = f"{original_id}_{uuid.uuid4().hex[:8]}"
            new_ids.append(new_id)
            existing_ids.add(new_id)

        self.collection.add(ids=new_ids, documents=texts, embeddings=embeddings)

    def query(self, query_text: str, top_k: int = 5) -> List[str]:
        """
        Truy vấn tìm kiếm văn bản gần nhất.

        Args:
            query_text (str): Văn bản truy vấn.
            top_k (int, optional): Số kết quả trả về. Mặc định là 5.

        Returns:
            List[str]: Danh sách các văn bản gần nhất.
        """
        query_embedding = self.embedding_model.embed_query(query_text)
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )
        return results["documents"][0] if "documents" in results else []


# # Ví dụ sử dụng:
# if __name__ == "__main__":
#     indexer = ChromaDBIndexer(collection_name="langchain")

#     # Thêm dữ liệu vào ChromaDB
#     texts = ["Hôm nay trời đẹp", "Tôi thích học AI", "LangChain rất thú vị"]
#     ids = ["1", "2", "3"]
#     indexer.add_texts(texts, ids)

#     # Truy vấn
#     query_result = indexer.query("Học máy là gì?")
#     print("Kết quả truy vấn:", query_result)
