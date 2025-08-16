FROM debian:bullseye

WORKDIR /app

RUN apt update && \
    apt install -y python3 pip python3-fontforge

COPY requirements.txt src/main.py /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3"]
