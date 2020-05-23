FROM python:3.8-slim

# Create this file so ptpython doesn't wait for input.
RUN mkdir /root/.ptpython
RUN touch /root/.ptpython/config.py

RUN apt-get -y update && apt-get -y install \
    libpq-dev \
    gcc \
    postgresql-client

RUN pip install -U \
    pip \
    pipenv

COPY Pipfile Pipfile.lock /app/

WORKDIR /app

RUN pipenv install --dev --system --deploy

COPY . /app

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["gunicorn", "carrick.wsgi:application"]

CMD ["--access-logfile", "-", "--reload", "--certfile", "localhost.crt", "--keyfile", "localhost.key"]
