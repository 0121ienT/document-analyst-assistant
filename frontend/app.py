import chainlit as cl
import requests
import asyncio

BASE_URL = "http://localhost:8000"  # Địa chỉ FastAPI server


@cl.on_chat_start
async def init():
    await cl.Message(
        content="""Hello! Welcome to Data Helper Chatbot!
        You can chat or attach a file using the paperclip icon."""
    ).send()


@cl.on_message
async def main(message: cl.Message):
    # Kiểm tra xem có file được attach không
    if message.elements:  # Nếu có file trong message
        for element in message.elements:
            if isinstance(element, cl.File):  # Xác nhận là file
                essage_content = "Bạn đợi chút nhé mình đang load tài liệu nhaaa . "
                msg = cl.Message(content="")
                await msg.send()
                for word in essage_content.split():
                    await msg.stream_token(word + " ")
                    await asyncio.sleep(0.15)  # Độ trễ giữa các từ
                await msg.update()
                await process_uploaded_file(element)
    else:  # Nếu chỉ có text
        try:
            response = requests.post(
                f"{BASE_URL}/chat", json={"text": message.content}, stream=True
            )
            print(f"Chat API status: {response.status_code}")
            response.raise_for_status()
            msg = cl.Message(content="")
            await msg.send()
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    await msg.stream_token(chunk.decode("utf-8"))
            await msg.update()
        except requests.exceptions.RequestException as e:
            await cl.Message(content=f"Lỗi khi gọi API: {str(e)}").send()


async def process_uploaded_file(file):
    try:
        # Đọc nội dung file từ đường dẫn tạm thời
        with open(file.path, "rb") as f:
            file_content = f.read()
        print(f"Sending file: {file.name}, size: {len(file_content)} bytes")

        # Gửi file lên API /upload-file/
        response = requests.post(
            f"{BASE_URL}/upload-file/",
            files={"file": (file.name, file_content, file.type)},
        )
        print(f"Upload API status: {response.status_code}, response: {response.text}")
        response.raise_for_status()

        message_content = f"Đã upload File {file.name} thành công . Bạn muốn hỏi gì ạ ."
        msg = cl.Message(content="")
        await msg.send()
        for word in message_content.split():
            await msg.stream_token(word + " ")
            await asyncio.sleep(0.15)  # Độ trễ giữa các từ
        await msg.update()
    except requests.exceptions.RequestException as e:
        print(f"Upload error: {str(e)}")
        await cl.Message(content=f"Lỗi khi upload file: {str(e)}").send()


@cl.on_stop
async def on_stop():
    await cl.Message(content="Phiên chat đã kết thúc.").send()
