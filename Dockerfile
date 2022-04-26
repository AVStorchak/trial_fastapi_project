FROM python:3.9

WORKDIR /code
COPY pyproject.toml .
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
COPY . .
EXPOSE 8000
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]