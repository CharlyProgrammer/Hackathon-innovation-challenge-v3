import json
import os 
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter



class processing():
    def __init__(self,book_paths):
        self.book_paths=book_paths
        
    def process_book_to_documents(self,book):
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
            # Procesing footnotes, images and tables from each chapter  
            for image in chapter.get("images", []):
                documents.append(
                    Document(
                        page_content=image['URL'],
                        metadata={**book_metadata, "type": "image_chapter", "chapter_title": chapter["title"],"image_title_chapter":image["title"],"page_image_chapter": image["page_number"]}
                    )
                )
            for table in chapter.get("tables", []):
                documents.append(
                    Document(
                        page_content=table['content'],
                        metadata={**book_metadata, "type": "table_chapter", "chapter_title": chapter["title"],"table_title_chapter":table["title"],"page_table_chapter": table["page_number"]}
                    )
                )
              
            for note in chapter.get("footnote", []):
                    documents.append(
                        Document(
                            page_content=note['content'],
                            metadata={**book_metadata, "type": "footnote_chapter", "chapter_title": chapter["title"],"footnote_title":note["title"],"page_footnote_chapter": note["page_number"]}
                        )
                    )
            # Procesing footnotes, images and tables from each subchapter              
            for subchapter in chapter.get("subchapters", []):
                subchapter_page = subchapter.get("page_number", "Unknown")
                documents.append(
                    Document(
                        page_content=subchapter["content"],
                        metadata={**book_metadata, "type": "subchapter","chapter_title": chapter["title"],"title_subchapter": subchapter["title"], "page_subchapter": subchapter_page}
                    )
                )
                
                for image in subchapter.get("images", []):
                    documents.append(
                        Document(
                            page_content=image['URL'],
                            metadata={**book_metadata, "type": "image_subchapter", "chapter_title": chapter["title"],"title_subchapter": subchapter["title"],"image_title_subchapter":image["title"],"page_image_subchapter": image["page_number"]}
                        )
                    )
                
                for table in subchapter.get("tables", []):
                    documents.append(
                        Document(
                            page_content=table['content'],
                            metadata={**book_metadata, "type": "table_subchapter", "chapter_title": chapter["title"],"title_subchapter": subchapter["title"], "table_title_subchapter":table["title"],"page_table_subchapter": table["page_number"]}
                        )
                    )
                for note in subchapter.get("footnote", []):
                    documents.append(
                        Document(
                            page_content=note['content'],
                            metadata={**book_metadata, "type": "footnote_subchapter", "chapter_title": chapter["title"],"title_subchapter": subchapter["title"],"footnote_title_subchapter":note["title"],"page_footnote_subchapter": note["page_number"]}
                        )
                    )    
        
        return documents
    
    def process_articles(self,article):
        article_data = []
        art_metadata = {
            "title": article["title"],
            "highlight": article["highlight"],
            "url": article["url"]
         
        }
        article_data.append(Document(page_content=article["content"],metadata={**art_metadata}))
        return article_data
    def split_docs(self,docs):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)
        return chunks
    
    def chunking_books(self,books):
        
        for book in books:
            chunking_docs=[]
            chunking_docs.append(self.split_docs(book))
        return chunking_docs
    
    def convert_docs(self):
        docs=[]
        
        for book_path in self.book_paths:
            with open(book_path, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            docs.append(self.process_book_to_documents(datos))    
        return docs