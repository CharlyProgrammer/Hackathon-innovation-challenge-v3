import reflex as rx 
from app.scripts_for_rag.scrap_video_data import extract_video_data
from app.styles import style_copilot
from app.scripts_for_rag.calls_models import model_completion
from app.scripts_for_rag.call_voice_models import voice_manager

import time
import os
class StateVideoAnalyzer(rx.State):
    title: str=""
    url:str=""
    video_text: str=""
    topic: str=""
    message_text:str=""
    response:str=""
    historial: list[tuple[str, str]]
    video_selector:str=""
    chat_field: str=""
    show_title: bool=False
    show_video: bool=False
    send_read_status: bool=False
    send_chat_status:bool=False
    voice_status: bool=False
    message_status: bool=False
    loading_state: bool=False
    loading_content_state:bool=False
    audio_loading_state: bool=False
    show_audio: bool=False
    video_urls:list[str]=[]
    video_titles: list[str]=[]
      
    @rx.event
            
    def update_selector_video(self,value:str):
        self.video_selector=value
        self.title=self.video_selector
          
        for idx,title in enumerate(self.video_titles):
            if self.video_selector==title:
                
                self.url=self.video_urls[idx]
                obj=extract_video_data()
                #get text from video
                self.video_text=obj.get_transcription(self.url)
                self.show_title=True
                self.show_video=True 
                self.send_chat_status=True
                self.send_read_status=True
                self.show_audio=False
                
    def change_mic_status(self):
        self.voice_status=True                
    def update_chat_field(self,value):
        self.chat_field=value    
    def init_loading(self):
        self.loading_state=True
    def init_content_loading(self):
        self.loading_content_state=True    
    def init_audio_loading(self):
        self.show_audio=False
        self.audio_loading_state=True
    def save_chat(self):
        try:
            answer=run_conversation(self.chat_field,self.video_text)
            self.response=answer
            self.loading_state=False
            self.historial.append((self.chat_field,answer))
            self.chat_field=""
            self.show_audio=False
        except Exception:
            answer="The topic of the selected article violates the principles of Reliability and safety of Responsible AI"
            self.response=answer
            self.loading_state=False
            self.historial.append((self.chat_field,answer))
            self.chat_field=""
            self.show_audio=False
                
    def save_voice(self):
        
                    
        voice_obj=voice_manager(key_speech_resource="SPEECH_KEY",region_speech_resource="SPEECH_REGION")
        client=voice_obj.init_voice_recognition()
        voice=voice_obj.convert_voice_text(speech_recognizer=client)
        if voice!="":
            try:
                answer=run_conversation(voice,self.video_text)
                self.response=answer
                self.historial.append((voice,answer))
                self.chat_field=""
                self.show_audio=False
                self.voice_status=False
            except Exception:
                answer="The topic of the selected article violates the principles of Reliability and safety of Responsible AI"
                self.response=answer
                self.loading_state=False
                self.historial.append((voice,answer))
                self.chat_field=""
                self.show_audio=False
                self.voice_status=False    
        else:
            voice="<!> Voice could't be detected, try again "
            self.response=answer
            self.historial.append((voice,""))
            self.chat_field=""
            self.show_audio=False
            self.voice_status=False
                    
              
            
    def send_text_read(self):
        
        if os.path.isfile("./uploaded_files/response.mp3"):
        
            os.remove("./uploaded_files/response.mp3") 
        name="response.mp3"
        out_path=rx.get_upload_dir()/name
        voice_obj=voice_manager(key_speech_resource="SPEECH_KEY",region_speech_resource="SPEECH_REGION")
        client=voice_obj.init_voice_generator(output_file=out_path)
        voice_obj.convert_text_voice(text=self.response,synthesizer=client,output_file=out_path)
        time.sleep(5)
        self.audio_loading_state=False
        self.show_audio=True
                   
    def update_topic_values(self,value:str):
        self.topic=value
        
    def load_articles_action(self):
        if self.topic!="":
            self.video_selector=""
            self.video_urls=[]
            self.video_titles=[]
            obj=extract_video_data()
            video_data=obj.get_video_search(self.topic)
            for video in video_data:
                self.video_urls.append(video["url"])
                self.video_titles.append(video["title"])
            
            self.message_status=False
            self.message_text=""
            self.loading_content_state=False
            self.send_chat_status=False
            self.send_read_status=False
            self.show_audio=False
            self.show_video=False
           
            
        else:
            self.video_selector=""
            self.video_urls=[]
            self.video_titles=[]
            self.topic=""
            self.message_text="<!> Error, topic field cannot be empty"
            self.message_status=True
            self.send_chat_status=False
            self.send_read_status=False
                            
    
    
    def back_action(self):
       
        self.video_selector=""
        self.video_urls=[]
        self.video_titles=[]
        self.historial=[]
        self.title=""
        self.topic=""
        self.show_audio=False
        self.show_video=False
        self.show_title=False
        self.send_chat_status=False
        self.send_read_status=False
        self.voice_status=False
        if os.path.isfile("./uploaded_files/response.mp3"):
        
            os.remove("./uploaded_files/response.mp3")
        return rx.redirect("/home/dashboard")

def run_conversation(user_prompt,context):
    #obj_llm_completion=model_completion("LLAMA_KEY","LLAMA_MODEL","OPENAI_KEY","OPENAI_MODEL","OPENAI_ENDPOINT")
    
    obj_llm_completion=model_completion(key_model_oa="OPENAI_KEY",endpoint_oa="OPENAI_ENDPOINT",model_version_oa="OPENAI_MODEL")
    messages=[{"role": "user","content": f"Based in the next context that is a video transcription:{context}, answer the next query:{user_prompt}"}]
    client=obj_llm_completion.init_model_openai()
    response=obj_llm_completion.generate_response_openai(client=client,messages=messages,temperature=0.8,max_tokens=800)
   
    return response

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(f"😀 USER: {question}", style=style_copilot.question_style),
            text_align="right",
        ),
        rx.box(
            rx.text(f"🤖 AI-BITS: {answer}", style=style_copilot.answer_style),
            text_align="left",
        ),
        margin_y="1em",
        width="100%",
    )
    
def chat() -> rx.Component:
    
    return rx.box(
        rx.foreach(
            StateVideoAnalyzer.historial,
            lambda messages: qa(messages[0], messages[1]),
        ),
        width="40vw"
        
         
    )

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=StateVideoAnalyzer.chat_field,
            placeholder="Make a question",
            on_change=StateVideoAnalyzer.update_chat_field, 
            style=style_copilot.input_style,
            background_color="white",
            height="4vh"
        ),
        rx.button(
            "Send",
            on_click=lambda:[StateVideoAnalyzer.init_loading,StateVideoAnalyzer.save_chat],
            style=style_copilot.button_style,
            height="4vh",
            
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            loading=StateVideoAnalyzer.loading_state,
            display=rx.cond(StateVideoAnalyzer.send_chat_status,"block","none")
        ),
        rx.button(
            rx.icon("mic"),
            background_color=rx.cond(StateVideoAnalyzer.voice_status,"red","blue"),
            on_click=lambda:[StateVideoAnalyzer.change_mic_status,StateVideoAnalyzer.save_voice],
            style=style_copilot.button_style,
            height="4vh",
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            
            display=rx.cond(StateVideoAnalyzer.send_chat_status,"block","none")
        ),
        rx.button(
            "Read",
            on_click=lambda:[StateVideoAnalyzer.init_audio_loading,StateVideoAnalyzer.send_text_read],
            style=style_copilot.button_style,
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            height="4vh",
            loading=StateVideoAnalyzer.audio_loading_state,
            display=rx.cond(StateVideoAnalyzer.send_read_status,"block","none")
        ),
        rx.box(
            rx.cond(
                StateVideoAnalyzer.show_audio,
                rx.audio(
                    url=rx.get_upload_url("response.mp3"),
                    width="400px",
                    height="32px",
           

                ),
                rx.box()
            )
        )
    )





        
def video_analyzer_page():
     return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(
                    
                    src="/logo.png",  # URL de la imagen
                    alt="Descripción de la imagen",
                    width="8vw",  # Ancho de la imagen
                    height="auto",   # Altura ajustada automáticamente
                    
                ),
                rx.heading(
                    'AI-BITS',
                                        
                    weight="bold",
                    high_contrast=True,
                    font_family="Times New Roman",
                    font_size="50px",
                    padding_left="5vw",
                    margin_top="2.5vh"
                   
                ),      
               
                
                padding_left="25vw",
                padding_right="5vw"
                
               
            
            ),
            
            rx.vstack(
                rx.heading(
                    "HACKATHON",
                    color_scheme="cyan",
                    weight="regular",
                    high_contrast=True,
                    font_family="Times New Roman",
                    font_size="24px",
                    
                
                ),
                rx.heading(
                    "INNOVATION CHALLENGE",
                    color_scheme="indigo",
                    weight="bold",
                    font_family="Times New Roman",
                    high_contrast=True,
                    font_size="2.5vh",
                    
                ),
                rx.heading(
                    "TECHLAB TEAM",
                    color_scheme="cyan",
                    weight="regular",
                    high_contrast=True,
                    font_family="Times New Roman",
                    font_size="2.5vh",
                    
                
                ),
                
                spacing='1px',
                
                
            
            ),
            
           
            padding_top="3vh",
            height="13vh",
            max_height='24vh',
            spacing="5px"
            
           
        ),
        rx.box(
            rx.flex(
                rx.heading(
                    "Volver",
                    color="white",
                    font_family="Arial",
                    font_size="20px",
                    cursor="pointer",
                    _hover={
                        "color": "cyan"  # Cambia el color del texto al pasar el cursor
                    },
                    on_click=StateVideoAnalyzer.back_action 
                ),
                
                spacing='60px',
                direction="row",
            ),
            
            display="flex", 
            alignItems="center",
            justifyContent="right",
            background_color="black",
            height="4vh",
            min_height='50px',
            max_height='100px',
            paddingX='12vw'
        ),
        rx.center(
            rx.box(
                rx.center(
                    rx.box(
                        
                        rx.heading(
                            "Welcome to the Video analyzer",
                            align="center",
                            font_family="Console",
                            font_size="38px",
                            weight="bold",
                            
                            style={
                                "text-shadow": "2px 2px 5px rgba(0, 0, 0, 0.5)"
                            }
                        
                        ),
                        rx.text(
                            "Transform how you interact with video content using the Video Analyzer. Search any topic, browse curated video titles, and dive into selected content with transcriptions and AI-driven Q&A. Experience hands-free interaction with voice input and audio output, redefining accessibility. Whether you're learning, researching, or just exploring, the Video Analyzer lets you unlock the secrets within every frame.",
                            style={
                                "padding-top": "20px",    
                                "padding-bottom": "16px",  
                                "padding-left": "8px",  
                                "padding-right": "8px"
                            },
                            font_family="Console",
                            font_size="150%",
                            text_align="justify",
                        ),
                        
                        
                    direction="column",
                    height="100%",
                    background_color="#E3E4E5",
                    width="90%",
                    paddingY='3vh',
                    border_color="black",  
                    border_width="2px",
                    spacing='8px'
                    ),
                    rx.box(
                        rx.heading("Instructions for 🎥 Video Analyzer",paddingX='1vw'),
                        rx.unordered_list(
                            rx.list_item(rx.text("Enter Your Preferred Topic: ",weight="bold"),rx.text("Begin your journey by typing your topic of interest in the designated search field. Let your curiosity guide you!")),
                            rx.list_item(rx.text("Load the Content: ",weight="bold"),rx.text("Click the 'Load Content' button, and watch as the system works its magic, fetching a curated list of video titles based on your chosen topic.")),
                            rx.list_item(rx.text("Choose Your Preferred Video: ",weight="bold"),rx.text("From the interactive list, select a video that sparks your interest. Upon selection, the system will display the video and its title, immersing you in the content.")),
                            rx.list_item(rx.text("Activate the AI features: ",weight="bold"),rx.text("If a transcription is available for the video, it will activate the chat with AI automatically. Use this feature to explore the video’s full narrative, enhancing your understanding about it.")),
                            rx.list_item(rx.text("Ask Your Questions: ",weight="bold"),rx.text("Unlock the power of AI! Whether you prefer typing in the chat or speaking via microphone, ask questions about the video’s content. The system processes your input and delivers insightful answers, either in text or through audio responses.")),                           
                            rx.list_item(rx.text("Inputs: ",weight="bold"),rx.text("For each new prompt or query, our system can process either a text input in the chat or an audio input through a microphone (just push the button and speak when it is in red)")),
                            rx.list_item(rx.text("Outputs: ",weight="bold"),rx.text("Like in the case of the inputs, our system can give either a text output in the chat or an audio output through a speaker element (just push the button 'READ' and wait it is ready, but sometimes it can take a few minutes)")),
                            paddingX='2vw',
                            paddingY="1vh"
                            

                        ),
                        rx.text("💡 Discover the Boundless Possibilities",weight="bold",paddingX='1vw'),
                        rx.text("The Video Analyzer combines cutting-edge AI with interactive features to bring video exploration to life. Dive deep into video content, ask insightful questions, and enjoy answers delivered in multiple formats. No limits, no barriers—just pure discovery.",paddingX='1vw'),
                        
                        
                    direction="column",
                    height="100%",
                    background_color="#E3E4E5",
                    width="90%",
                    paddingY='3vh',
                    
                   
                    ),
                    
                    rx.form(
                        rx.text(
                            'Topic to search',
                            align='left',
                            font_family="Times New Roman",
                            font_size="16px",
                            weight="bold",
                            style={
                                "padding-top": "5px",    # Padding superior
                                "padding-bottom": "5px",  # Padding inferior
                                "padding-left": "20vw",  # Padding inferior
                                "padding-right": "8px"
                            }
                        ),
                        rx.box(
                            rx.input(
                                width='50%',
                                value=StateVideoAnalyzer.topic,
                                placeholder="Write the topic to search",
                                on_change=StateVideoAnalyzer.update_topic_values, 
                                
                            ),
                            style={
                                "display": "flex",  # Activa Flexbox
                                "flexDirection": "column",  # Alinea elementos en columna
                                "justifyContent": "center",  # Centrado vertical
                                "alignItems": "center",  # Centrado horizontal
                                "height": "3vh",  # Altura del formulario
                                # Opcional: bordes del formulario
                            },
                        ),
                        rx.box(
                            rx.button(
                                "Load content",
                                font_family="Console",
                                width='30%',
                                cursor='pointer',
                                font_size="20px",
                                _hover={
                                    "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
                                },
                                on_click=lambda:[StateVideoAnalyzer.init_content_loading,StateVideoAnalyzer.load_articles_action],
                                loading=StateVideoAnalyzer.loading_content_state,
                                style={
                                    "background-color": "#1A237E",
                                    "height": "4vh",
                                    "border-radius": "10px", 
                                    "marginTop": "20px",
                                    "marginBottom": "20px",
                                    "display": "flex",
                                    "justifyContent": "center",
                                },
                            ),
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                                "gap": "10px",  # Espaciado uniforme entre elementos
                                "alignItems": "center",
                            },
                        ),
                        rx.center(
                            rx.text(
                                StateVideoAnalyzer.message_text,
                                color="red",
                                font_family="Times New Roman",
                                font_size="18px",
                                weight="bold",
                                padding_bottom="2vh",
                                display=rx.cond(StateVideoAnalyzer.message_status,"block","none")
                                
                            ),
                        ),    
                        rx.center(
                            rx.fragment(
                                rx.select.root(
                                    rx.select.trigger(color_scheme='blue',variant='soft', placeholder="Select a video"),
                                    rx.select.content(
                                        rx.select.group(
                                            rx.foreach(
                                                StateVideoAnalyzer.video_titles,
                                                lambda x: rx.select.item(
                                                    x, value=x
                                                ),
                                            )
                                        ),
                                        color_scheme='amber',
                                        variant='solid'
                                    ),
                                    value=StateVideoAnalyzer.video_selector,
                                    on_change=StateVideoAnalyzer.update_selector_video,
                                    size='3'
                                
    ,
                                )                       
                            )
                        )    
                    ),
                    rx.box(
                        
                        rx.heading(
                            StateVideoAnalyzer.title,
                            align="center",
                            font_family="Console",
                            font_size="38px",
                            weight="bold",
                        
                        ),
                        direction="column",
                        height="10vh",
                        background_color="#E3E4E5",
                        width="90%",
                        paddingY='3vh',
                        border_color="black",  # Color del borde
                        border_width="2px",
                        display=rx.cond(StateVideoAnalyzer.show_title,"block","none")
                  
                    ),
                    
                    
                   
                    
                    rx.box(
                        rx.center(
                            rx.video(
                                url=StateVideoAnalyzer.url,
                                width="30vw",
                                height="30vh",
                            ),
                        ),    
                        direction="column",
                        height="fit-content",
                        background_color="#E3E4E5",
                        width="90%",
                        paddingY='3vh',
                        border_color="black",  # Color del borde
                        border_width="2px",
                        display=rx.cond(StateVideoAnalyzer.show_video,"block","none")
                  
                    ),
                    rx.box(
                        rx.center(
                            rx.heading(
                            "Chat with the article",
                            align="center",
                            font_family="Console",
                            font_size="38px",
                            weight="bold",
                        
                        )
                        ),
                        rx.center(
                    
                            rx.vstack(
                                chat(),
                                action_bar(),
                                align="center",
                            ),
                            padding="2vw"
                            
                        ),
                        direction="column",
                        height="100%",
                        background_color="#E3E4E5",
                        width="90%",
                        paddingY='3vh',
                   
                    ),
                    spacing='40px',
                    direction="column",
                    paddingY='3vh'
                ), 
                
                direction="column",
                height="100%",
                background_color="#FCF9ED",
                width="80%",
            
            ),
            
            background_color="#e2d2c3",
            width="100%",
            height='100%'
            
        ),    
        
    height="100%",
    width="100%",
    )

