FROM python:3.11.1 as base

WORKDIR /src
RUN apt-get -y upgrade && \
    apt-get -y update && \
    apt-get install -y wkhtmltopdf
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY .. .

ENV PYTHONPATH /src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
