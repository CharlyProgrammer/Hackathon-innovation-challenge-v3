import json
import os 
import re

book_path='Data/book_abc_electricity.json'
out_path='Data/book_abc_electricity_plain.json'
libro=dict()
# Cargar archivo JSON original
with open(book_path, "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)
    libro["id"]=datos["id"]
    libro["general_title"]=datos["general_title"]
    libro["author"]=datos["author"]
    libro["publisher"]=datos["publisher"]
    libro["year"]=datos["year"]
    libro["total_pages"]=datos["total_pages"]
    libro["type_book"]=datos["type_book"]
    



  
for id,chapter in enumerate(datos["chapters"]):
    libro[f"chapter_title_{id+1}"]=chapter["title"]
    libro[f"chapter_content_{id+1}"]=chapter["content"] 
    libro[f"page_number_chapter{id+1}"]=chapter["page_number"]
    for idf,figure in enumerate(chapter.get("images",[])):
        libro[f"image_title_{idf+1}_chapter_{id+1}"]=figure["title"]
        libro[f"image_url_{idf+1}_chapter_{id+1}"]=figure["URL"] 
        libro[f"page_number_{idf+1}_chapter_{id+1}"]=figure["page_number"]
    for idsc, subchapter in enumerate(chapter.get("subchapters",[])):
        libro[f"subchapter_title_{idsc+1}_chapter_{id+1}"]=subchapter["title"]
        libro[f"subchapter_content__{idsc+1}_chapter_{id+1}"]=subchapter["content"] 
        libro[f"subchapter_page_number_{idsc+1}_chapter_{id+1}"]=subchapter["page_number"] 
        for idf,figure in enumerate(subchapter.get("images",[])):
            libro[f"image_title_{idf+1}_chapter_{id+1}_subchapter{idsc+1}"]=figure["title"]
            libro[f"image_url_{idf+1}_chapter_{id+1}_subchapter{idsc+1}"]=figure["URL"] 
            libro[f"page_number_{idf+1}_chapter_{id+1}_subchapter{idsc+1}"]=figure["page_number"]
        for idf,footnote in enumerate(subchapter.get("footnote",[])):
            libro[f"footnote_title_{idf+1}_chapter_{id+1}_subchapter{idsc+1}"]=footnote["title"]
            libro[f"footnote_content_{idf+1}_chapter_{id+1}_subchapter{idsc+1}"]=footnote["content"] 
            libro[f"footnote_page_number_{idf+1}_chapter_{id+1}_subchapter{idsc+1}"]=footnote["page_number"]      


with open(out_path, "w", encoding="utf-8") as archivo_formateado:
    json.dump(libro, archivo_formateado, ensure_ascii=False,indent=4)
