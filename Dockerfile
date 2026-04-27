FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install uv && uv sync

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "run_server.py"]