FROM python:3.9.9

WORKDIR /api

COPY poetry.lock /api/
COPY pyproject.toml /api/
COPY app/ /api/app

RUN python -m pip install poetry
RUN poetry install

CMD [ "poetry", "run", \
"gunicorn", \
"-w", "8", \
"-b", "0.0.0.0:8888", \
"-k", "uvicorn.workers.UvicornWorker", \
"app.main:app", \
"--access-logfile", "-", \
"--log-config", "gunicorn_logging.ini"]
