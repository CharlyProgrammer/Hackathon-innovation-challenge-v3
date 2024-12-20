from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
import azure.cognitiveservices.speech as speechsdk
from pytube import YouTube
from moviepy.audio.io import AudioFileClip
import time
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.dirname(os.getcwd())+'/innovation_challenge_v3/app/scripts_for_rag/.env')
class extract_video_data:
    def __init__(self,key_speech_resource,region_speech_resource):
        self.driver_path="D:\proyectos de lenguajes de programacion\python\drivers/geckodriver.exe"
        self.options = Options()
        self.options.add_argument("--headless") 
        self.driver=Service(self.driver_path)
        self.web_service=webdriver.Firefox(service=self.driver,options=self.options)
        self.key_speech_resource=key_speech_resource
        self.region_speech_resource=region_speech_resource
    
        
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
    
    
  
obj=extract_video_data(key_speech_resource="SPEECH_KEY",region_speech_resource="SPEECH_REGION")        
data= obj.get_video_search("roman empire")
print(data[0]["url"])        
        

    