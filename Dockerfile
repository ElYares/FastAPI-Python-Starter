# Imagen oficial de Python
FROM python:3.11-slim

# Variables para evitar mensajes de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Setea directorio de trabajo
WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Instala dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Exposición del puerto
EXPOSE 8000

# Comando para levantar el server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

