FROM python:3.10

WORKDIR /frontend

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install chainlit

COPY frontend/ .

EXPOSE 8001
CMD ["chainlit", "run", "app.py", "--port", "8001"]
