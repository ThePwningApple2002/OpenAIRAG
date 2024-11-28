from scrapper import *
from database import *
from embeddings import *
import numpy as np
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

name = "Macke"

VECTOR_DIMENSIONS = 384
# pretraga  = search_fn(name, 5)
# extract = extract_content(pretraga)
# splitovan = split(extract)
# embed_prokleti = embed(splitovan)

r = connect_to_redis()

INDEX_NAME = "index"                              # Vector Index Name
DOC_PREFIX = "doc:"  
# instantiate a redis pipeline
pipe = r.pipeline()

# define some dummy data
objects = [
    {"name": "a", "tag": "foo"},
    {"name": "b", "tag": "foo"},
    {"name": "c", "tag": "bar"},
]

# write data
for obj in objects:
    # define key
    key = f"doc:{obj['name']}"
    # create a random "dummy" vector
    obj["vector"] = np.random.rand(VECTOR_DIMENSIONS).astype(np.float32).tobytes()
    # HSET
    pipe.hset(key, mapping=obj)

res = pipe.execute()

query = (
    Query("*=>[KNN 2 @vector $vec as score]")
     .sort_by("score")
     .return_fields("id", "score")
     .return_field("vector", decode_field=False) # return the vector field as bytes
     .paging(0, 2)
     .dialect(2)
)

query_params = {
    "vec": np.random.rand(VECTOR_DIMENSIONS).astype(np.float32).tobytes()
}
print(r.ft("index").search(query, query_params).docs)
# store_embeddings(r, embed_prokleti, name)


