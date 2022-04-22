FROM python:3.9

WORKDIR /code
COPY pyproject.toml .
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
COPY . .
RUN uvicorn app:app --reload