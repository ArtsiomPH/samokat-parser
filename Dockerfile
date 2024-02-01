ARG PYTHON_VERSION=3.11.5

FROM python:${PYTHON_VERSION}-slim

RUN mkdir -p /app
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl

# ~~~~~~~~ Virtualenv ~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./pyproject.toml ./poetry.lock ./

ENV PATH "${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false

RUN poetry install  --no-interaction --no-ansi


COPY . .

CMD ["sh", "./start.sh"]