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
path = ""

document = {"path": path, "file":0, "hash":to_hash(path) , "last_detected": datetime.now(), "last_scaned": datetime.now() - timedelta(days=100), "last_updated": datetime.now() - timedelta(days=100) }

# Добавление документа в коллекцию
result = collection.insert_one(document)

# создание индекса
collection.create_index("hash", unique=True)
collection.create_index("last_detected")
collection.create_index("last_updated")
collection.create_index("last_scaned")
collection.create_index("file")
collection.create_index([('path', 'text')], default_language='russian')