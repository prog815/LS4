FROM mongo:latest

# install Python 3
RUN apt-get update 
RUN apt-get install -y python3
RUN apt-get -y install python3-dev
RUN apt-get install -y python3-pip
RUN pip3 install pymongo


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

# Create an administrative user and enable authentication
EXPOSE 27017

# Create a root user with a password
RUN mongod --fork --logpath /var/log/mongodb.log && \
    sleep 10 && \
    echo 'use admin; db.createUser({user: "root", pwd: "password", roles: ["root"]})' | mongosh && \
    python3 init_base.py && \
    mongod --dbpath /data/db --shutdown

CMD mongod --bind_ip_all & python3 ./app.py

