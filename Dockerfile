FROM python:3.13.0


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt ./
COPY .env ./

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8001

CMD ["uvicorn", "hackathon.app:app", "--host", "0.0.0.0", "--port", "8001"]