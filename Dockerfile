FROM python:3.8

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . /app

CMD python manage.py runserver 0.0.0.0:8000