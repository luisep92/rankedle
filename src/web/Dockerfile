FROM python:3.11-slim

WORKDIR /app

# Avoid some problems
ENV POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

# Install poetry/dependencies
RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Setup the working directory
WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --only web --no-root

# Copy project files
COPY ./src/web .

# Expose port 8000
EXPOSE 8000

# Set entrypoint to run initial actions
ENTRYPOINT ["/app/entrypoint.sh"]

# Run webserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
