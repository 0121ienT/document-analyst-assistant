from domain.rag_pipeline import IRAGPipeline
from .indexing import ChromaDBIndexer
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()


class RAGPipeline(IRAGPipeline):
    async def process(self, user_message: str):
        indexer = ChromaDBIndexer(collection_name="langchain")
        context = indexer.query(user_message)
        template = """Bạn là một ứng dụng AI cho phép người dùng gửi các nguồn thông tin lên và hỏi đáp thông tin của các nguồn đó.\n
        Nội dung của context bên dưới chính là nội dung của các nguồn được gửi, hãy đọc nó cẩn thận và trả lời câu hỏi nhé.
        - Sử dụng câu ngắn gọn, tự nhiên , thân thiện gần gũi nhưng không quá sến súa.\n
        - Nếu câu hỏi không rõ, hãy hỏi lại thay vì giả định sai.\n
        - Đừng lặp lại câu từ cứng nhắc từ câu hỏi.\n
        Hãy suy nghĩ từng bước, bạn có thể lấy thêm context bên dưới để trả lời câu hỏi dưới đây một cách chính xác và nhớ giải thích từng bước \n

        Context:\n
        {context}\n

        Question: \n
        {question}\n

        Người phát triển bạn: Nguyễn Thị Vân - Mã sinh viên: 2021601412
        """

        prompt = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )

        llm = ChatOpenAI(
            model_name=os.getenv("MODEL_OPENAI_NAME"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.5,
            streaming=True,
            max_tokens=4096,
        )

        # Chain
        rag_chain = (
            RunnableMap(
                {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
            )
            | prompt
            | llm
            | StrOutputParser()
        )

        async for chunk in rag_chain.astream(
            {"context": context, "question": user_message}
        ):
            yield chunk


class FAQPipeline(IRAGPipeline):
    async def process(self, user_message: str):
        template = """
        Hãy suy nghĩ từng bước để trả lời câu hỏi dưới đây một cách chính xác và nhớ giải thích từng bước \n

        Question: \n
        {question}"""

        prompt = PromptTemplate(template=template, input_variables=["question"])

        llm = ChatOpenAI(
            model_name=os.getenv("MODEL_OPENAI_NAME"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.5,
            streaming=True,
            max_tokens=4096,
        )

        # Chain
        rag_chain = (
            RunnableMap(
                {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
            )
            | prompt
            | llm
            | StrOutputParser()
        )

        async for chunk in rag_chain.astream({"question": user_message}):
            yield chunk
