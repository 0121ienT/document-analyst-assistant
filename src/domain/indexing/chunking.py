from typing import List, Dict, Any
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
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
            model: str = os.getenv("MODEL_EMBEDDEING")
            buffer_size: int = kwargs.get("buffer_size", 1)
            breakpoint_threshold_amount: int = kwargs.get("breakpoint_threshold_amount", 70)
            embedding_model = OpenAIEmbeddings(model=model)
            self.chunker = SemanticChunker(
                buffer_size=buffer_size,
                breakpoint_threshold_amount=breakpoint_threshold_amount,
                embeddings=embedding_model
            )

        elif method == "character":
            chunk_size: int = kwargs.get("chunk_size", 1000)
            chunk_overlap: int = kwargs.get("chunk_overlap", 200)
            self.chunker = CharacterTextSplitter(
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap
            )

        elif method == "recursive":
            chunk_size: int = kwargs.get("chunk_size", 1000)
            chunk_overlap: int = kwargs.get("chunk_overlap", 200)
            self.chunker = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap
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
        if self.method == "semantic":
            chunks = self.chunker.create_documents(text)
            return [chunk.page_content for chunk in chunks]
        else:
            return self.chunker.split_text(text)


# # =========================
# # 📌 Ví dụ sử dụng
# # =========================

# docs = """Hôm nay là một ngày tuyệt vời để bắt đầu bằng một tách cà phê nóng hổi. 
# Sau khi thưởng thức bữa sáng, tôi quyết định đi dạo trong công viên gần
# nhà, nơi cây cối xanh tươi và tiếng chim hót rộn ràng. Tuy nhiên, tôi hơi
# thất vọng vì công viên khá đông đúc, khiến không khí yên bình thường ngày
# bị phá vỡ. Mặc dù vậy, tôi vẫn tìm được một góc nhỏ yên tĩnh để đọc cuốn
# sách yêu thích. Sau buổi sáng trong lành, tôi quay về nhà để làm việc. 
# Công việc hôm nay khá bận rộn, nhưng tôi cảm thấy rất hài lòng vì hoàn 
# thành được một dự án lớn. Buổi tối, tôi tự thưởng cho mình một bữa ăn ngon
# và xem một bộ phim hài trước khi đi ngủ."""

# # Chunking theo ngữ nghĩa
# semantic_chunker = TextChunker(method="semantic")
# chunks_semantic = semantic_chunker.chunk(docs)
# print("📌 Chunking theo ngữ nghĩa:")
# for i, chunk in enumerate(chunks_semantic):
#     print(f"Chunk {i+1}:\n{chunk}\n")

# # Chunking theo ký tự (fixed-size character splitting)
# char_chunker = TextChunker(method="character", chunk_size=150, chunk_overlap=30)
# chunks_character = char_chunker.chunk(docs)
# print("📌 Chunking theo ký tự:")
# for i, chunk in enumerate(chunks_character):
#     print(f"Chunk {i+1}:\n{chunk}\n")

# # Chunking theo recursive character splitting
# recursive_chunker = TextChunker(method="recursive", chunk_size=150, chunk_overlap=30)
# chunks_recursive = recursive_chunker.chunk(docs)
# print("📌 Chunking theo recursive character splitting:")
# for i, chunk in enumerate(chunks_recursive):
#     print(f"Chunk {i+1}:\n{chunk}\n")
