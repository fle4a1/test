FROM python:3.12-slim

EXPOSE 7070

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH="${PYTHONPATH}:/project/app"

RUN apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*  &&  apt-get clean
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN pip install poetry

COPY pyproject.toml poetry.lock* ./
RUN --mount=type=ssh poetry install --with scheduler
COPY app app
RUN mkdir logs
RUN mkdir schedules

CMD ["sh", "-c", "aerich init-db && aerich upgrade && python app/main.py scheduler"]