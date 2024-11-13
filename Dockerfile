FROM python:3.13.0

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip

RUN pip install .

EXPOSE 8000

CMD ["uvicorn", "hackathon.app:app", "--host", "0.0.0.0", "--port", "8000"]
