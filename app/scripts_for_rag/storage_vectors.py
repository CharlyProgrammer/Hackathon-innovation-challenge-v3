import os
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import chromadb
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

class storage:
    
    def __init__(self,chunks_books):
        self.chunks_books=chunks_books
         
    def transform_chunks_books(self):
        EmbedChunk_book=[]
        EmbedChunks_books=[]
        get_embeddings=self.load_embedModel()
        for chunks_book in self.chunks_books:
            for chunk in chunks_book:
                embed_chunk=get_embeddings.embed_query(chunk.page_content)
                EmbedChunk_book.append(embed_chunk)
        EmbedChunks_books.append(EmbedChunk_book)       
        return EmbedChunks_books
    
    def load_embedModel(self):
        embeddings = FastEmbedEmbeddings(model_name="intfloat/multilingual-e5-large")
        return embeddings 
    def init_chromaDB(self):
        client = chromadb.HttpClient(
                      host="localhost",
                      port=8000,
                      ssl=False,
                      headers=None,
                      settings=Settings(),
                      tenant=DEFAULT_TENANT,
                      database=DEFAULT_DATABASE,
                )
        return client
    
    def collecting_data(self,chunks_docs,chunkembed_docs):
        content_chunks=[]
        metadata_chunks=[]
        embeddings_chunks=[]
        id_chunks=[]
        for book_idx,(chunks_of_book,embedd_books) in enumerate(zip(chunks_docs,chunkembed_docs)):
            for chunk_idx,(chunk,emb_chunk) in enumerate(zip(chunks_of_book,embedd_books)):
                content_chunks.append(chunk.page_content)
                metadata_chunks.append(chunk.metadata)
                embeddings_chunks.append(emb_chunk)
                id_chunks.append(f"book_{book_idx+1}_chunk_{chunk_idx+1}")
                
        return content_chunks,metadata_chunks,embeddings_chunks,id_chunks       
    def storage_chunks_books(self):
            EmbedChunks_books=self.transform_chunks_books()
            client_chroma=self.init_chromaDB()
            collection = client_chroma.get_or_create_collection(name="library")
            content,metadata,embeddings,ids=self.collecting_data(self.chunks_books,EmbedChunks_books)
            collection.add(
                documents=content,
                embeddings=embeddings,
                metadatas=metadata,
                ids=ids
            )
         
            

           