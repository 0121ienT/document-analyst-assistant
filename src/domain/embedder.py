import os
from typing import List, Union
from langchain_openai.embeddings import OpenAIEmbeddings
import numpy as np

class Embedder:
    """
    Lớp hỗ trợ tính toán embedding cho văn bản trong quá trình indexing.
    """

    def __init__(self) -> None:
        """
        Khởi tạo bộ embedding với mô hình OpenAI từ biến môi trường.
        """
        model = os.getenv("MODEL_EMBEDDEING")  # Mặc định nếu MODEL không được đặt
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key is None:
            raise ValueError("API key không được tìm thấy. Hãy thiết lập biến môi trường OPENAI_API_KEY.")

        self.model: str = model
        self.embedder = OpenAIEmbeddings(model=model, openai_api_key=api_key)

    def embed_text(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Tạo embedding từ văn bản đầu vào.

        Args:
            text (Union[str, List[str]]): Văn bản hoặc danh sách văn bản.

        Returns:
            Union[List[float], List[List[float]]]: Vector embedding của văn bản.
        """
        if isinstance(text, str):
            return self.embedder.embed_query(text)
        elif isinstance(text, list):
            return self.embedder.embed_documents(text)
        else:
            raise TypeError("Đầu vào phải là chuỗi hoặc danh sách chuỗi.")

    def index_texts(self, texts: List[str]) -> np.ndarray:
        """
        Nhận danh sách văn bản và trả về mảng embeddings.

        Args:
            texts (List[str]): Danh sách văn bản cần indexing.

        Returns:
            np.ndarray: Mảng chứa embeddings của tất cả văn bản.
        """
        embeddings = self.embedder.embed_documents(texts)
        return np.array(embeddings)

# Ví dụ sử dụng
if __name__ == "__main__":
    try:
        indexer = Embedder()
        texts = ["Hôm nay là một ngày đẹp trời.", "Tôi thích đọc sách vào buổi sáng."]
        embeddings = indexer.index_texts(texts)
        print("Embedding của danh sách văn bản:", embeddings.shape)
    except ValueError as e:
        print(f"Lỗi: {e}")
