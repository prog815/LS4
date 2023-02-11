FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN wget https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js
RUN mv jquery.min.js ./static/
RUN pip3 install -r requirements.txt

CMD python ./app.py