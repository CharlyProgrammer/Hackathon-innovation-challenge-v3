from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.dirname(os.getcwd())+'/innovation_challenge_v3/app/scripts_for_rag/.env')
class voice_manager:
    def __init__(self,key_speech_resource,region_speech_resource):
        self.key_speech_resource=key_speech_resource
        self.region_speech_resource=region_speech_resource
       
    
    def init_voice_generator(self,output_file):
        key=os.getenv(self.key_speech_resource)
        region=os.getenv(self.region_speech_resource)
        speech_config = SpeechConfig(subscription=key, region=region)
        audio_config = AudioConfig(filename=str(output_file))
        synthesizer = SpeechSynthesizer(speech_config=speech_config,audio_config=audio_config)
        return synthesizer    
    
    def convert_text_voice(self,synthesizer,text,output_file):
        
        
        result = synthesizer.speak_text_async(text).get()
        output_file="./uploaded_files/response.mp3"
       
        if result.reason == result.reason.SynthesizingAudioCompleted:
            print(f"Archivo de audio generado: {output_file}")
            
           
        elif result.reason == result.reason.Canceled:
            print("Error en la síntesis del texto a audio:", result.error_details)

           