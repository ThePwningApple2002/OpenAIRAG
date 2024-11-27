from scrapper import *
from database import *
from embeddings import *


name = "Recipe for a pie"

pretraga  = search_fn(name, 5)
extract = extract_content(pretraga)
splitovan = split(extract)
embed_prokleti = embed(splitovan)

print(embed_prokleti, embed_prokleti.shape)

r = connect_to_redis()

store_embeddings(r, embed_prokleti, name)

