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
        # truy van du lieu
        indexer = ChromaDBIndexer(collection_name="langchain")
        context = indexer.query(user_message)
        # tao prompt tu docs
        template = """Bạn là một trợ lý AI thông minh được phát triển bởi Nguyễn Thị Vân, mã sinh viên là 2021601412,
        trường Công Nghệ Thông tin và Truyền thông  và là sinh viên được hướng dẫn bởi Thạc Sĩ Nguyễn Thanh Hùng
        của trường đại học Công nghiệp Hà Nội, bạn thân thiện và giao tiếp tự nhiên
        như con người. Hãy phản hồi giống như một người bạn đang trò chuyện, sử
        dụng ngôn ngữ tự nhiên, thân thiện, và tránh quá cứng nhắc.
        - Sử dụng câu ngắn gọn, tự nhiên , thân thiện gần gũi nhưng không quá sến súa.
        - Nếu câu hỏi không rõ, hãy hỏi lại thay vì giả định sai.
        - Đừng lặp lại câu từ cứng nhắc từ câu hỏi.

        Context:
        {context}

        Question: {question}"""

        prompt = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )

        llm = ChatOpenAI(
            model_name=os.getenv("MODEL_OPENAI_NAME"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.8,
            streaming=True,
            max_tokens=5000,
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
