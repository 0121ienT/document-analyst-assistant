import os
import shutil
import chainlit as cl
from chainlit.types import ThreadDict
import requests
import asyncio

# from dotenv import load_dotenv
# load_dotenv()

BASE_URL = "http://localhost:8000"


async def process_uploaded_file(file):
    try:
        with open(file.path, "rb") as f:
            file_content = f.read()
        print(f"Sending file: {file.name}, size: {len(file_content)} bytes")

        response = requests.post(
            f"{BASE_URL}/upload-file/",
            files={"file": (file.name, file_content, file.type)},
        )
        print(f"Upload API status: {response.status_code}, response: {response.text}")
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Upload error: {str(e)}")
        await cl.Message(content=f"Lỗi khi upload file: {str(e)}").send()


@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    if current_user.metadata["role"] != "admin":
        return None
    return [
        cl.ChatProfile(
            name="GPT-4o-mini",
            markdown_description="The underlying LLM model is **GPT-4o-mini and answer everyday question**.",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="NotebookGPT",
            markdown_description="The underlying LLM model is **GPT-4o-mini and answer question based on file**.",
            icon="https://picsum.photos/250",
        ),
    ]


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == (
        os.getenv("CHAINLIT_USERNAME"),
        os.getenv("CHAINLIT_PASSWORD"),
    ):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


# files = None
@cl.on_chat_start
async def init():
    user = cl.user_session.get("user")
    chat_profile = cl.user_session.get("chat_profile")
    if chat_profile == "GPT-4o-mini":
        await cl.Message(
            content=f"""✨ Hello {user.identifier}! ✨
                Welcome! We're excited to have you here, starting your session with the **"{chat_profile}"** chat profile tailored just for you."""
        ).send()
    else:
        files = None
        while files is None:
            files = await cl.AskFileMessage(
                content=f"""✨ Hello {user.identifier}! ✨
                Welcome! We're excited to have you here, starting your session with the **"{chat_profile}"** chat profile tailored just for you."""
                + """📂 To get started, please upload the document you'd like me to assist with.
                We currently support the following file types:
                • 📄 `.txt` – Plain text files
                • 📑 `.pdf` – PDF documents
                • 📊 `.xlsx`, `.xls` – Excel spreadsheets
                • 📝 `.docx`, `.doc` – Word documents
                Simply drag and drop your file here or click to upload — I’ll take care of the rest. Let’s dive in!
                """,
                accept=[
                    "text/plain",
                    "text/csv",
                    "application/pdf",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "application/vnd.ms-excel",  # .xls
                ],
                max_size_mb=50,
                max_files=10,
                timeout=300,
                raise_on_timeout=True,
            ).send()
        for i in range(len(files)):
            await process_uploaded_file(files[i])
            message_content = f"`{files[i].name}` uploaded, let's ask us some question!"
            msg = cl.Message(content="")
            await msg.send()
            for word in message_content.split():
                await msg.stream_token(word + " ")
                await asyncio.sleep(0.15)
            await msg.update()


@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)


@cl.on_message
async def main(message: cl.Message):
    chat_profile = cl.user_session.get("chat_profile")
    if chat_profile == "NotebookGPT":
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
            await cl.Message(content=f"API meet an error: {str(e)}").send()
    else:
        try:
            response = requests.post(
                f"{BASE_URL}/chat-faq", json={"text": message.content}, stream=True
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
            await cl.Message(content=f"API meet an error: {str(e)}").send()


@cl.on_stop
async def on_stop():
    await cl.Message(content="The chat has been stopped.").send()


@cl.on_chat_end
def on_chat_end():
    chroma_db_path = "chroma_db"
    if os.path.exists(chroma_db_path) and os.path.isdir(chroma_db_path):
        shutil.rmtree(chroma_db_path)
        print("✅ Đã xóa thư mục chroma_db")
    else:
        print("⚠️ Thư mục chroma_db không tồn tại hoặc không phải là thư mục")
    # global files
    # files = None
    print("The user disconnected!")


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    print("The user resumed a previous chat session!")
