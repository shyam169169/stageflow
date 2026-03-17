FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy project
COPY . .

EXPOSE 8000

CMD ["uvicorn", "stageflow.api.app:app", "--host", "0.0.0.0", "--port", "8000"]