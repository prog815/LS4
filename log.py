import pandas as pd
import pymongo

# Подключение к MongoDB
client = pymongo.MongoClient()
db = client['loc-search']
collection = db['log']

# Запрос данных из коллекции log
data = pd.DataFrame(list(collection.find())).drop('_id', axis=1)

# Вывод данных в стандартный вывод в формате CSV
print(data.to_csv(index=False))
