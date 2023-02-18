

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