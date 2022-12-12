FROM python:3.11.1-bullseye as base

WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY .. .

ENV PYTHONPATH /src

CMD ["python3", "-m", "pais_worker"]
