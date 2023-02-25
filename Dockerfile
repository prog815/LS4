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
COPY init_db.sh /docker-entrypoint-initdb.d/

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install pandas

RUN apt-get install wget
RUN apt-get install nano
RUN apt-get install cron

RUN export PATH=$PATH:/usr/bin/python3

# Create an administrative user and enable authentication
EXPOSE 27017

RUN touch /app/update.log
RUN echo "* * * * * cd /app; python3 scan.py > /home/update.log 2>&1" > /app/crontab
RUN crontab /app/crontab

CMD service cron start & mongod --bind_ip_all & python3 ./app.py
