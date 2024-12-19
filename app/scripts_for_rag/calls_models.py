from dotenv import load_dotenv
import os
from openai import AzureOpenAI  
from langchain_groq import ChatGroq
load_dotenv(dotenv_path=os.path.dirname(os.getcwd())+'/innovation_challenge_v3/app/scripts_for_rag/.env')

class model_completion:
    def __init__(self,key_model_llama="",model_version_llama="",key_model_oa="",model_version_oa="", endpoint_oa=""):
       
        self.key_model_llama=key_model_llama
        self.model_version_llama=model_version_llama
        self.key_model_oa=key_model_oa
        self.model_version_oa=model_version_oa
        self.endpoint_oa=endpoint_oa
        self.llama_key=""
        self.llama_client=""
        self.llama_model=""
        self.openai_key=""
        self.openai_client=""
        self.openai_endpoint=""
        self.openai_model=""
        
    def init_llama_model(self,temperature,max_tokens):
              
        self.llama_key = os.getenv(self.key_model_llama)
        self.llama_model = os.getenv(self.model_version_llama)
        self.llama_client = ChatGroq(
            model=self.llama_model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=None,
            max_retries=2,
            api_key= self.llama_key
            
        )
        return self.llama_client
    
    def init_model_openai(self):
        
        self.openai_endpoint = os.getenv(self.endpoint_oa)
        self.openai_key=os.getenv(self.key_model_oa)
        self.openai_model = os.getenv(self.model_version_oa)
        
        client = AzureOpenAI(  
        
        azure_endpoint= self.openai_endpoint,  

        api_key= self.openai_key,  

        api_version="2024-05-01-preview",  

        )
        
        return client  
    
    def generate_response_llama(self,client,messages):
        
       
        response=client.invoke(messages)
        return response.content
    
    
    def generate_response_openai(self,client,messages,temperature,max_tokens):
        #self.openai_model = os.getenv(self.model_version_oa)
        print(self.openai_model)
        response = client.chat.completions.create(  

                    model=self.openai_model,  
                    messages=messages,  
                    max_tokens=max_tokens,  
                    temperature=temperature,  
                    top_p=0.95,  
                    frequency_penalty=0,  
                    presence_penalty=0,  
                    stop=None,  
                    )  

                

        return response.choices[0].message.content