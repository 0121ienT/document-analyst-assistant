from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

def get_embedding(text: str, embeddings_model=None) -> list:
    """
    Nhúng một đoạn văn bản thành vector sử dụng `.embed_query` của LangChain.

    Args:
        text (str): Văn bản cần nhúng.
        embeddings_model (optional): Mô hình embeddings, mặc định là OpenAIEmbeddings.

    Returns:
        list: Vector nhúng của văn bản đầu vào.
    """
    if embeddings_model is None:
        embeddings_model = OpenAIEmbeddings(model=os.getenv("MODEL"), openai_api_key=os.getenv("OPENAI_API_KEY"))  # Mặc định sử dụng OpenAIEmbeddings
    
    return embeddings_model.embed_query(text)

# # Ví dụ sử dụng với OpenAIEmbeddings
# vector = get_embedding("What was the name mentioned in the conversation?")

# # In ra 5 giá trị đầu tiên của vector nhúng
# print(vector[:5])
