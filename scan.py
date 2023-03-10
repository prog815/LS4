import lib
from datetime import datetime,timedelta

import os
from pymongo import MongoClient
import time


# устанавливаем соединение с базой данных MongoDB
client = MongoClient("mongodb://localhost:27017/")

# выбираем нужную базу данных и коллекцию
db = client["loc-search"]
collection = db["files"]

# Создание первого документа
path = ""

document = {"path": path, 
            "file": 0, 
            "hash": lib.to_hash(path), 
            "last_detected": datetime.now(), 
            "last_scaned": datetime.now() - timedelta(days=100), 
            "last_updated": datetime.now() - timedelta(days=100),
            "modification": datetime.now() - timedelta(days=100),
            "size": 0}

try:
    # Добавление документа в коллекцию
    result = collection.insert_one(document)
    # создание индекса
    collection.create_index("hash", unique=True)
    collection.create_index("last_detected")
    collection.create_index("last_updated")
    collection.create_index("last_scaned")
    collection.create_index("file")
    collection.create_index([('path', 'text')], default_language='russian')
except:
    pass

# вычисляем дату 
days_ago = datetime.now() - timedelta(days=3)

# создаем фильтр для поиска файлов, где file=0 и last_scaned меньше чем 
filter = {"file": 0, "last_scaned": {"$lt": days_ago}}

# устанавливаем ограничение на количество результатов - не более 10
limit = 60

# создаем проекцию для вывода только полей _id и path
projection = {"_id": 1, "path": 1}

# выполняем поиск с помощью метода find() и ограничиваем количество результатов с помощью метода limit()
results = collection.find(filter,projection).limit(limit)
print(filter)
# выводим результаты
for result in results:
    
    # прерываем, если больше минуты работаем
    if lib.run_time() > 60:
        break
    
    print('-'*40)
    print(result)
    path = result['path']
    _id = result['_id']
    try:
        
        with os.scandir("./static/files/" + path) as it:
            
            for entry in it:
                p = entry.path[15:].replace('\\','/')
                
                h = lib.to_hash(p)
                
                if entry.is_dir():
                    try:
                        # добавляем новый каталог в базу
                        document = {"path": p, 
                                    "file":0, 
                                    "hash":h , 
                                    "last_detected": datetime.now(), 
                                    "last_scaned": datetime.now() - timedelta(days=100), 
                                    "last_updated": datetime.now() - timedelta(days=100),
                                    "modification": datetime.fromtimestamp(os.path.getmtime(entry.path)),
                                    "size": 0}
                        collection.insert_one(document)
                        print('new dir: ' + p)
                    except:
                        result = collection.update_one({"hash": h}, {"$set": {"last_detected": datetime.now(),
                                                                              "modification": datetime.fromtimestamp(os.path.getmtime(entry.path))}})
                        print('updated dir: ' + p + " with result: " + str(result.modified_count))
                elif entry.is_file():
                    try:
                        # добавляем новый файл в базу
                        document = {"path": p, 
                                    "file":1, 
                                    "hash":h , 
                                    "last_detected": datetime.now(), 
                                    "last_scaned": datetime.now() - timedelta(days=100),
                                    "last_updated": datetime.now() - timedelta(days=100),
                                    "modification": datetime.fromtimestamp(os.path.getmtime(entry.path)),
                                    "size": os.path.getsize(entry.path)}
                        collection.insert_one(document)
                        print('new file: ' + p)
                    except:
                        result = collection.update_one({"hash": h}, {"$set": {"last_detected": datetime.now(),
                                                                              "modification": datetime.fromtimestamp(os.path.getmtime(entry.path)),
                                                                              "size": os.path.getsize(entry.path)}})
                        print('updated file: ' + p + " with result: " + str(result.modified_count))
        
        # удачное сканирование папки
        result = collection.update_one({"_id": _id}, {"$set": {"last_scaned": lib.date_plus_random_delta(datetime.now()),
                                                               "last_updated": datetime.now()}})
        print('success updated dir: ' + path + " with result: " + str(result.modified_count))
    except:
        # неудачное сканирование папки
        result = collection.update_one({"_id": _id}, {"$set": {"last_scaned": lib.date_plus_random_delta(datetime.now())}})
        print('неудачно : ' + path + " with result: " + str(result.modified_count))
    
    time.sleep(1)
    
