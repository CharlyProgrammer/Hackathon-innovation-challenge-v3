from transform_docs import processing
#from storage_vectors import storage
import os 

books_paths=[
    os.path.dirname(os.getcwd())+'/innovation_challenge_v3/Data/book_abc_electricity.json'
    ]
processing_obj=processing(books_paths)                
docs=processing_obj.convert_docs()
chunking_from_books=processing_obj.chunking_books(docs)
print(chunking_from_books[0][323])
#storage_obj=storage(chunking_from_books)
#obj_storage=storage(chunking_from_books)
#obj_storage.storage_chunks_books()

