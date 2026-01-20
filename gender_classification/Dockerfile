# 1. Base image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY inference/ ./inference/
COPY artifacts/ ./artifacts/

# 6. Expose Flask port
EXPOSE 8000

# 7. Run the Flask app
CMD ["python", "inference/app.py"]
