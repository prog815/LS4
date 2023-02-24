import os
from datetime import datetime,timedelta

with os.scandir("./static") as it:
    for entry in it:
        print(datetime.fromtimestamp(os.path.getmtime(entry.path)))
