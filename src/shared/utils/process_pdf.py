from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


def process_pdf(documents, embedding_model=None):
    print(f"Nhận {len(documents)} tài liệu để xử lý.")
    if not documents:
        print("Không có tài liệu nào để xử lý!")
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(documents)
    print(f"Số đoạn văn bản sau khi chia nhỏ: {len(splits)}")

    embedding_model = embedding_model or OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        splits, embedding=embedding_model, persist_directory="./chroma_db"
    )
    vectorstore.persist()

    print(f"ChromaDB hiện có {vectorstore._collection.count()} vector.")
    return vectorstore.as_retriever()
