FROM python:3.11-slim

# Establece variables de entorno para evitar problemas con Poetry
ENV POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

# Instala Poetry y dependencias del sistema
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root
RUN apt-get update && apt-get install -y ffmpeg

# Copia los archivos del proyecto

COPY . .

# Instala las dependencias del proyecto


# Comando por defecto para ejecutar la aplicación

CMD ["python", "/app/src/rankedle/bot.py"]