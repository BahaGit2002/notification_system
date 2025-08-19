FROM python:3.11-slim

RUN pip install --no-cache-dir poetry

WORKDIR /code

COPY pyproject.toml poetry.lock* /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY . /code

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
