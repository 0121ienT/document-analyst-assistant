FROM python:3.12-slim

WORKDIR /frontend

COPY uv.lock pyproject.toml /frontend/

RUN pip install --no-cache-dir uv

RUN pip install --no-cache-dir chainlit

COPY frontend/ .

RUN uv sync

EXPOSE 8002

CMD ["chainlit", "run", "app.py", "--port", "8002"]
