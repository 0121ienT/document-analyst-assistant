from typing import List, Dict, Any
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
import os


class TextChunker:
    """
    Lớp hỗ trợ chunking văn bản với nhiều phương pháp khác nhau.
    """

    def __init__(self, method: str = "semantic", **kwargs: Any) -> None:
        """
        Khởi tạo bộ chia văn bản với phương pháp được chọn.

        Args:
            method (str): Phương pháp chunking, có thể là:
                - "semantic": Chunk theo ngữ nghĩa với OpenAI embeddings dùng với dữ liệu phi cấu trúc.
                - "character": Chunk theo ký tự cố định, phù hợp với dữ liệu có cấu trúc đơn giản.
                - "recursive": Chunk theo recursive character splitting, có thể dùng với dữ liệu bán cấu trúc.
            **kwargs (Any): Các tham số bổ sung cho phương pháp chunking.
        """
        self.method: str = method
        self.kwargs: Dict[str, Any] = kwargs

        if method == "semantic":
            print("we are using semantic chunking !!!\n")
            model: str = os.getenv("MODEL_EMBEDDING")
            buffer_size: int = kwargs.get("buffer_size", 1)
            breakpoint_threshold_amount: int = kwargs.get(
                "breakpoint_threshold_amount", 70
            )
            embedding_model = OpenAIEmbeddings(model=model)
            self.chunker = SemanticChunker(
                buffer_size=buffer_size,
                breakpoint_threshold_amount=breakpoint_threshold_amount,
                embeddings=embedding_model,
            )

        elif method == "character":
            print("we are using character chunking !!!\n")
            chunk_size: int = kwargs.get("chunk_size", 1000)
            chunk_overlap: int = kwargs.get("chunk_overlap", 200)
            self.chunker = CharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )

        elif method == "recursive":
            print("we are using recursive chunking !!!\n")
            chunk_size: int = kwargs.get("chunk_size", 1000)
            chunk_overlap: int = kwargs.get("chunk_overlap", 200)
            self.chunker = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )

        else:
            raise ValueError(f"Phương pháp chunking '{method}' không được hỗ trợ!")

    def chunk(self, text: str) -> List[str]:
        """
        Chia văn bản thành các đoạn theo phương pháp đã chọn.

        Args:
            text (str): Văn bản cần chunk.

        Returns:
            List[str]: Danh sách các đoạn văn bản sau khi chunk.
        """
        with open("output_chunk.txt", "w", encoding="utf-8") as f:
            f.write(" ".join(text))
        if self.method == "semantic":
            chunks = self.chunker.create_documents(text)
            return [chunk.page_content.replace("\n", " ") for chunk in chunks]
        else:
            return self.chunker.split_text(text)
