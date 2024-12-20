from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
import azure.cognitiveservices.speech as speechsdk
import os
import time
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
    
    def init_voice_recognition(self):
        key=os.getenv(self.key_speech_resource)
        region=os.getenv(self.region_speech_resource)
        speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        speech_config.speech_recognition_language = "en-US"  # Configura el idioma a inglés (Estados Unidos)

        # Configura el reconocimiento con un tiempo de espera
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        return speech_recognizer
    
    def convert_text_voice(self,synthesizer,text,output_file):
        
        
        result = synthesizer.speak_text_async(text).get()
        output_file="./uploaded_files/response.mp3"
       
        if result.reason == result.reason.SynthesizingAudioCompleted:
            print(f"Audio file successful generated in: {output_file}")
            
           
        elif result.reason == result.reason.Canceled:
            print("Error, audio file could't be generated:", result.error_details)

    def convert_voice_text(self,speech_recognizer):
        

        # Ejecuta el reconocimiento y espera hasta obtener un resultado o un silencio
        result = speech_recognizer.recognize_once_async().get()

        # Maneja el resultado según su estado
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
          
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            
            return ""
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Reconocimiento cancelado: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Detalles del error: {cancellation_details.error_details}")
            return ""
    
