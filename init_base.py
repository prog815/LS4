from pymongo import MongoClient
from datetime import datetime,timedelta

from lib import to_hash

# Установка соединения с сервером MongoDB
client = MongoClient('localhost', 27017)

# Установка соединения с базой данных
db = client['loc-search']

# Установка соединения с коллекцией
collection = db['files']

# Создание документа
path = "/"

document = {"path": path, "hash":to_hash(path) , "last_detected": datetime.utcnow(), "last_updated": (datetime.now() - timedelta(days=3)).utcnow() }

# Добавление документа в коллекцию
result = collection.insert_one(document)

# создание индекса
collection.create_index("hash", unique=True)
collection.create_index("last_detected")
collection.create_index("last_updated")
