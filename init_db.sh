mongod --fork --logpath /var/log/mongodb.log && \
sleep 10 && \
echo 'use admin; db.createUser({user: "root", pwd: "password", roles: ["root"]})' | mongosh && \
python3 init_base.py && \
mongod --dbpath /data/db --shutdown