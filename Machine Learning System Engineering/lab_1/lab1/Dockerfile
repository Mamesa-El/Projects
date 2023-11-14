ARG APP_DIR=/APP_DIR

FROM python:3.10-slim as build
ARG APP_DIR

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install curl -y \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/POETRY_HOME
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./
RUN python -m venv --copies ${APP_DIR}/venv
RUN . /${APP_DIR}/venv/bin/activate && poetry install --only main

FROM python:3.10-slim as deploy
ARG APP_DIR

WORKDIR ${APP_DIR}
COPY --from=build ${APP_DIR}/venv ${APP_DIR}/venv
ENV PATH=${APP_DIR}/venv/bin:${PATH}

COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]