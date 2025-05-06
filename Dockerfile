FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 6. Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# 7. Default command
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "skillbase.wsgi:application", "--bind", "0.0.0.0:8000"]
