FROM python:3.14-slim

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY .env.example ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY api api/
COPY cli cli/
COPY config config/
COPY core core/
COPY messaging messaging/
COPY providers providers/
COPY smoke smoke/
COPY server.py ./

# Create workspace directory
RUN mkdir -p agent_workspace

# Create env file from example
RUN cp .env.example .env

EXPOSE 8082

CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8082"]