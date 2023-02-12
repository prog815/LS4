# FROM python:3.8-alpine

# WORKDIR /app

# COPY . /app

# --------------------------------------------------------

FROM mongo:latest

# install Python 3
RUN apt-get update 
RUN apt-get install -y python3
RUN apt-get -y install python3-dev
RUN apt-get install -y python3-pip
RUN pip3 install pymongo

# EXPOSE 27017
# Set the working directory
WORKDIR /app

# Copy the files from the host to the container
COPY . /app

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get install wget

RUN wget https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js
RUN mv jquery.min.js ./static/
# RUN pip3 install -r requirements.txt

RUN export PATH=$PATH:/usr/bin/python3
# RUN which python3

CMD mongod & python3 ./app.py

# CMD python3 ./app.py

# --------------------------------------------------------

# FROM python:3.8

# RUN apt-get update && apt-get install -y gnupg

# RUN apt-get install -y wget

# RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -

# RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# RUN apt-get update

# RUN apt-get install -y mongodb-org

# WORKDIR /app

# COPY . /app

# CMD ["mongod"]


