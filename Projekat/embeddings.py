from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def split(text):

    if isinstance(text, str): 
        documents = [Document(page_content=text)]
    elif isinstance(text, list):
        documents = [Document(page_content=doc) if isinstance(doc, str) else doc for doc in text]
    else:
        raise ValueError("Input should be a string or a list of strings/Documents.")
    

    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    

    chunks = splitter.split_documents(documents)
    return chunks

def embed(documents):
    texts = [doc.page_content for doc in documents]
    return model.encode(texts)