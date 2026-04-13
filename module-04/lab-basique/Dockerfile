# ✅ BON ordre — pip install mis en cache si requirements.txt n'a pas changé
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .              
RUN pip install --no-cache-dir -r requirements.txt
COPY . .                             
CMD ["python", "app.py"]
