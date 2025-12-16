FROM python:3.11-slim

WORKDIR /app

# Copy the full project before installing, so the `engine` package exists
COPY . .

RUN pip install --upgrade pip && \
    pip install .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



