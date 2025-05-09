FROM python:3.10

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN pip install uv

RUN uv sync

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
