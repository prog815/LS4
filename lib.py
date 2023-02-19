import time

# -------------------------------------------------------------

def time_now():
    '''
    текущее время в секундах
    '''
    return int(time.time())

# -------------------------------------------------------------

start_time = time_now()

def run_time():
    '''
    время в секундах от запуска программы
    '''
    return time_now() - start_time

# -------------------------------------------------------------

def date_plus_random_delta(d):
    import random
    import datetime
    
    delta_hours = random.randint(0, 23)
    delta_minutes = random.randint(0, 59)
    delta_seconds = random.randint(0, 59)
    delta = datetime.timedelta(hours=delta_hours, minutes=delta_minutes, seconds=delta_seconds)
    return d + delta

def to_hash(s):
    import hashlib
    seed = '123456'
    
    # Create a hash function instance with the seed value
    hash_func = hashlib.sha256(seed.encode())
    
    # Update the hash function with the input string
    hash_func.update(s.encode())

    # Get the hash value
    hash_value = hash_func.digest()
    
    return hash_value

