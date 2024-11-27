import redis
import numpy as np

def connect_to_redis(host='localhost', port=6379, db=0):
    try:
        r = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        # Test the connection
        if r.ping():
            print("Connected to Redis")
        return r
    except redis.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
        return None

def create_redis_index(r, vector_dim, vector_type="FLAT"):
    r.execute_command(
        "FT.CREATE",
        "embedding_index",
        "ON", "HASH",
        "PREFIX", "1", "embedding:",  # Prefix for keys
        "SCHEMA",
        "vector", "VECTOR", vector_type,  # Vector field
        "6",  # Number of arguments for VECTOR
        "TYPE", "FLOAT32",
        "DIM", vector_dim,  # Dimension of embeddings
        "DISTANCE_METRIC", "COSINE"  # Similarity metric
    )

def store_embeddings(r, embeddings, name):
    for i, vector in enumerate(embeddings):
        embedding_bytes = np.array(embeddings, dtype=np.float32).tobytes()
        r.hset(f"{name}:{i}", mapping={"vector": embedding_bytes})
# vector_dim = 384  # Replace with the size of your embedding vectors
# create_redis_index(r, vector_dim)
# CRUD Operations
def create_value(r, key, value):
    """Create a new key-value pair in Redis."""
    try:
        result = r.set(key, value)
        if result:
            print(f"Key '{key}' set successfully.")
        else:
            print(f"Failed to set key '{key}'.")
    except Exception as e:
        print(f"Error creating value: {e}")


# def create_value_loop(r, keys, values):
#       """Create a new key-value pair in Redis."""
#     try:
#         result = r.set(key, value)
#         if result:
#             print(f"Key '{key}' set successfully.")
#         else:
#             print(f"Failed to set key '{key}'.")
#     except Exception as e:
#         print(f"Error creating value: {e}")


def read_value(r, key):
    """Read the value of a given key."""
    try:
        value = r.get(key)
        if value is not None:
            print(f"Value for key '{key}': {value}")
        else:
            print(f"Key '{key}' does not exist.")
    except Exception as e:
        print(f"Error reading value: {e}")

def update_value(r, key, value):
    """Update the value of an existing key."""
    try:
        if r.exists(key):
            r.set(key, value)
            print(f"Key '{key}' updated successfully.")
        else:
            print(f"Key '{key}' does not exist.")
    except Exception as e:
        print(f"Error updating value: {e}")

def delete_value(r, key):
    """Delete a key from Redis."""
    try:
        if r.delete(key):
            print(f"Key '{key}' deleted successfully.")
        else:
            print(f"Key '{key}' does not exist.")
    except Exception as e:
        print(f"Error deleting value: {e}")

