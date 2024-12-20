from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable
import time
import os
import re
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.dirname(os.getcwd())+'/innovation_challenge_v3/app/scripts_for_rag/.env')
class extract_video_data:
    def __init__(self):
        self.driver_path="D:\proyectos de lenguajes de programacion\python\drivers/geckodriver.exe"
        self.options = Options()
        self.options.add_argument("--headless") 
        self.driver=Service(self.driver_path)
        self.web_service=webdriver.Firefox(service=self.driver,options=self.options)
       
    
        
    def get_video_search(self,topic:str):
        url_base='https://www.youtube.com/results?search_query='
        topic=topic.replace(" ","+")
        url=url_base+topic
        self.web_service.get(url)
        time.sleep(5)
        video_elements = self.web_service.find_elements(By.CSS_SELECTOR, "a#video-title")
        results = []
        for video in video_elements:
            title = video.get_attribute("title")  # Obtener el título del video
            url = video.get_attribute("href")    # Obtener la URL del video
            
            if title and url:  # Asegurarse de que ambos existan
                results.append({"title": title, "url": url})
        
        return results
    
    
    def get_video_id(self,url):
        pattern = r'(?:v=|be/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            raise ValueError("URL no admitted or it doesn't contain a video ID")

    def get_transcription(self,video_url):
    
        try:
            video_id = self.get_video_id(video_url)
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
            except Exception:
                # Si falla, obtener la transcripción en el primer idioma disponible
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_transcript([t.language for t in transcript_list]).fetch()
            transcription_text = "\n".join([item['text'] for item in transcript])
            transcription_text=transcription_text.replace("\xa0","")
            return transcription_text

        except ValueError as ve:
            return f"Error: {ve}"
        except TranscriptsDisabled:
            return "Error: The transcriptions are not activate for this video"
        except VideoUnavailable:
            return "Error: The video isn't available."
        except Exception as e:
            return f"Unexpected error: {e}"   
    


