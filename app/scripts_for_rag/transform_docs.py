import json
import os 
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

books_path=[
    os.path.dirname(os.getcwd())+'/Proyecto_de_fase_3/Datos/Historia/libros/electricity_book.json'
    ]
def process_book_to_documents(book):
    documents = []
    book_metadata = {
        "id": book["id"],
        "general_title": book["general_title"],
        "author": book["author"],
        "publisher": book["publisher"],
        "year": book["year"],
        "total_pages":book["total_pages"],
        "type_book":book["type_book"] 
    }

    for chapter in book["chapters"]:
        chapter_page = chapter.get("page_number", "Unknown")
        documents.append(
            Document(
                page_content=chapter["content"],
                metadata={**book_metadata, "type": "chapter","chapter_title": chapter["title"], "chapter_page": chapter_page}
            )
        )
        # Procesar imágenes y tablas del capítulo
        for image in chapter.get("images", []):
            documents.append(
                Document(
                    page_content=image['URL'],
                    metadata={**book_metadata, "type": "image_chapter", "image_title":image["title"],"page_number": image["page_number"]}
                )
            )
        for table in chapter.get("tables", []):
            documents.append(
                Document(
                    page_content=table['content'],
                    metadata={**book_metadata, "type": "table_chapter","table_title":table["title"],"page_number": table["page_number"]}
                )
            )
        for subchapter in chapter.get("subchapters", []):
            subchapter_page = subchapter.get("page_number", "Unknown")
            documents.append(
                Document(
                    page_content=subchapter["content"],
                    metadata={**book_metadata, "type": "subchapter","title_subchapter": subchapter["title"], "page_number": subchapter_page}
                )
            )
            
            for image in subchapter.get("images", []):
                documents.append(
                    Document(
                        page_content=image['URL'],
                        metadata={**book_metadata, "type": "image_subchapter", "image_title":image["title"],"page_number": image["page_number"]}
                    )
                )
            
            for table in subchapter.get("tables", []):
                documents.append(
                    Document(
                        page_content=table['content'],
                        metadata={**book_metadata, "type": "table_subchapter", "table_title":table["title"],"page_number": table["page_number"]}
                    )
                )
    
    return documents
# Cargar archivo JSON original
docs=[]
for book_path in books_path:
    with open(book_path, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    docs.append(process_book_to_documents(datos))    

#print(docs[0])

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    return chunks

chunking_docs=split_docs(docs[0])

print(chunking_docs[15])      