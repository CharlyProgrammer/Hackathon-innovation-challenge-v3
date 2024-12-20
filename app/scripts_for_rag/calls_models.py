from dotenv import load_dotenv
import os
from openai import AzureOpenAI  

load_dotenv(dotenv_path=os.path.dirname(os.getcwd())+'/innovation_challenge_v3/app/scripts_for_rag/.env')

class model_completion:
    def __init__(self,key_model_oa="",model_version_oa="", endpoint_oa=""):
       
        self.key_model_oa=key_model_oa
        self.model_version_oa=model_version_oa
        self.endpoint_oa=endpoint_oa
        self.openai_key=""
        self.openai_endpoint=""
        self.openai_model=""
        
       
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
    
        
    def generate_response_RAG_openai(self,client,messages,temperature,max_tokens):
        endpoint_search=os.getenv("SEARCH_ENDPOINT")
        index_name=os.getenv("SEARCH_INDEX")
        key=os.getenv("SEARCH_KEY")
        response = client.chat.completions.create(  

                        model=self.openai_model,  
                        messages=messages,  
                        max_tokens=max_tokens,  
                        temperature=temperature,  
                        top_p=0.95,  
                        frequency_penalty=0,  
                        presence_penalty=0,  
                        stop=None,
                        extra_body={  
                            "data_sources": [  
                                {  
                                    "type": "azure_search",  
                                    "parameters": {  
                                        "endpoint": endpoint_search,  
                                        "index_name": index_name,  
                                        "authentication": {
                                            "type": "api_key",
                                            "key": key
                                        }  
                                    }  
                                }  
                            ]  
                        }  
                    )  

        print(response.choices[0].message.content)        

        return response.choices[0].message.content
    
    def generate_response_openai(self,client,messages,temperature,max_tokens):
       
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

