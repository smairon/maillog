FROM python:3.12-slim

ENV MUSL_LOCPATH=en_US.utf8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

WORKDIR /opt/app/

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
COPY poetry.lock pyproject.toml /opt/app/
RUN poetry config virtualenvs.create false && poetry install --no-dev

ADD . /opt/app

ENTRYPOINT ["python", "cli.py"]