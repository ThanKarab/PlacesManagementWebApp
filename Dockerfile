FROM python:3.8.10

#######################################################
# Setting up env variables and workdir
#######################################################
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    APP_PATH=/opt/places \
    DB_PATH=/opt/db

ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONPATH="/opt"
WORKDIR $APP_PATH

#######################################################
# Installing poetry and dependencies
#######################################################
RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev


COPY ./places $APP_PATH
VOLUME $DB_PATH
EXPOSE 8000

CMD poetry run python manage.py migrate && poetry run python manage.py runserver 0.0.0.0:8000
