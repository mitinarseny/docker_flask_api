FROM python:3.7.0-slim-stretch

ADD . /code/
WORKDIR /code

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api:app"]