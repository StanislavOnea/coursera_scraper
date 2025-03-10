FROM python:3.12-slim

WORKDIR /usr/src/scraper

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD ["python3", "lambda_function.py"]
