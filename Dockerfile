# 1. Use compatible Python version
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements first (layer caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY api/ ./api/
COPY models/ ./models/

# 6. Expose Flask port
EXPOSE 5000

# 7. Set environment variables
ENV FLASK_APP=api/app.py
ENV PYTHONUNBUFFERED=1

# 8. Run Flask app
CMD ["python", "api/app.py"]
