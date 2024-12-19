from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
import requests
import time
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
    
    def transcribe_from_url(api_key, region, audio_url):
        speech_config = SpeechConfig(subscription=api_key, region=region)
        audio_config = AudioConfig(filename=audio_url)
        
        recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        
        try:
            result = recognizer.recognize_once()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return result.text
            else:
                print("No se pudo reconocer el discurso.")
                return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
obj=extract_video_data()        
data= obj.get_video_search("azure ai search")
print(len(data))        
        

    