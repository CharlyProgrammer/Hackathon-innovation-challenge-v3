import reflex as rx 
from app.scripts_for_rag.scrap_data import extract_web_data
from app.styles import style_copilot
from app.scripts_for_rag.calls_models import model_completion
from app.scripts_for_rag.call_voice_models import voice_manager
import time
import os
class StateImgAnalyzer(rx.State):
    
    img: str=""
    response:str=""
    title: str=""
    text_bloq1:str=""
    text_bloq2: str=""
    topic: str=""
    message_text:str=""
    historial: list[tuple[str, str]]
    image_selector: str = ""
    article_selector:str=""
    chat_field: str=""
    show_audio: bool=False
    show_image:bool=False
    show_title: bool=False
    send_read_status: bool=False
    send_chat_status:bool=False
    message_status: bool=False
    voice_status: bool=False
    audio_loading_state: bool=False
    loading_state: bool=False
    articles_urls:list[str]=[]
    articles_titles: list[str]=[]
    images_article:list[str]=[]
    images_urls:list[str]=[]
    
    @rx.event
            
    def update_image_selector(self, value: str):
        """Change the select value var."""
        self.image_selector = value
        self.send_chat_status=True
        self.send_read_status=True
        self.show_image=True
        self.show_audio=False
        for idx,image in enumerate(self.images_article):
            if self.image_selector==image:
                self.img=self.images_urls[idx]
                  
    def update_chat_field(self,value):
        self.chat_field=value    
    def init_loading(self):
         self.loading_state=True
    
    def change_mic_status(self):
        self.voice_status=True        
    def init_audio_loading(self):
        self.show_audio=False
        self.audio_loading_state=True
    
    def save_chat(self):
        try:
            answer=run_conversation(self.chat_field,self.img)
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
                answer=run_conversation(voice,self.img)
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
            
    def update_selector_article(self,value:str):
        self.article_selector=value
        self.title=self.article_selector
        self.show_title=True
        self.images_article=[]
        self.images_urls=[]
        self.image_selector=""
       
        obj=extract_web_data()
        
        for idx,article in enumerate(self.articles_titles):
            if self.article_selector==article:
                
                url=self.articles_urls[idx]
                images_data,port=obj.get_article_images(url)
                if port!="":
                    self.images_urls.append(port)
                for url in images_data:
                    self.images_urls.append(url.attrs["src"])
                
                for i in range(len(self.images_urls)):
                    self.images_article.append(f"image {i+1}")
                   
    def update_topic_values(self,value:str):
        self.topic=value
        
    def load_articles_action(self):
        if self.topic!="":
            self.image_selector=""
            self.article_selector=""
            self.images_article=[]
            self.images_urls=[]
            self.articles_urls=[]
            self.articles_titles=[]
            obj=extract_web_data()
            urls,titles=obj.get_articles_search(self.topic)
            self.articles_urls=urls
            self.articles_titles=titles
            self.message_status=False
            self.message_text=""
            self.send_chat_status=False
            self.send_read_status=False
            self.show_audio=False
        else:
            self.image_selector=""
            self.article_selector=""
            self.images_urls=[]
            self.articles_urls=[]
            self.articles_titles=[]
            self.topic=""
            self.message_text="<!> Error, topic field cannot be empty"
            self.message_status=True
            self.send_chat_status=False
            self.send_read_status=False                   
    
    
    def back_action(self):
        self.image_selector=""
        self.article_selector=""
        self.show_title=False
        self.images_urls=[]
        self.articles_urls=[]
        self.articles_titles=[]
        self.historial=[]
        self.img=""
        self.title=""
        self.topic=""
        self.show_image=False
        self.send_chat_status=False
        self.send_read_status=False
        self.show_audio=False
        if os.path.isfile("./uploaded_files/response.mp3"):
        
            os.remove("./uploaded_files/response.mp3")
        return rx.redirect("/home/dashboard")

def run_conversation(user_prompt,img_url):
    #obj_llm_completion=model_completion("LLAMA_KEY","LLAMA_MODEL","OPENAI_KEY","OPENAI_MODEL","OPENAI_ENDPOINT")
    
    obj_llm_completion=model_completion(key_model_oa="OPENAI_KEY",endpoint_oa="OPENAI_ENDPOINT",model_version_oa="OPENAI_MODEL_VISION")
    messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url
                        }
                    }
                ]
            }]
    client=obj_llm_completion.init_model_openai()
    response=obj_llm_completion.generate_response_openai(client=client,messages=messages,temperature=0.8,max_tokens=800)
    #client=obj_llm_completion.init_model_openai()
    #response=obj_llm_completion.generate_response_openai(client=client,prompt=user_prompt,temperature=0.7)
    return response

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=style_copilot.question_style),
            text_align="right",
        ),
        rx.box(
            rx.text(answer, style=style_copilot.answer_style),
            text_align="left",
        ),
        margin_y="1em",
        width="100%",
    )
    
def chat() -> rx.Component:
    
    return rx.box(
        rx.foreach(
            StateImgAnalyzer.historial,
            lambda messages: qa(messages[0], messages[1]),
        ),
        width="40vw"
        
         
    )

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=StateImgAnalyzer.chat_field,
            placeholder="Make a question",
            on_change=StateImgAnalyzer.update_chat_field, 
            style=style_copilot.input_style,
            background_color="white",
            height="4vh"
        ),
        rx.button(
            "Send",
            on_click=lambda:[StateImgAnalyzer.init_loading,StateImgAnalyzer.save_chat],
            style=style_copilot.button_style,
            height="4vh",
            loading=StateImgAnalyzer.loading_state,
            display=rx.cond(StateImgAnalyzer.send_chat_status,"block","none")
        ),
        rx.button(
            rx.icon("mic"),
            background_color=rx.cond(StateImgAnalyzer.voice_status,"red","blue"),
            on_click=lambda:[StateImgAnalyzer.change_mic_status,StateImgAnalyzer.save_voice],
            style=style_copilot.button_style,
            height="4vh",
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            
            display=rx.cond(StateImgAnalyzer.send_chat_status,"block","none")
        ),
        rx.button(
            "Read",
            on_click=lambda:[StateImgAnalyzer.init_audio_loading,StateImgAnalyzer.send_text_read],
            style=style_copilot.button_style,
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            height="4vh",
            loading=StateImgAnalyzer.audio_loading_state,
            display=rx.cond(StateImgAnalyzer.send_read_status,"block","none")
        ),
        rx.box(
            rx.cond(
                StateImgAnalyzer.show_audio,
                rx.audio(
                    url=rx.get_upload_url("response.mp3"),
                    width="400px",
                    height="32px",
           

                ),
                rx.box()
            )
        )
    )





        
def image_analyzer_page():
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
                    "INNOVATION CHALLENGE DICEMBER",
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
                    on_click=StateImgAnalyzer.back_action 
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
                            "Welcome to the image analyzer",
                            align="center",
                            font_family="Console",
                            font_size="38px",
                            weight="bold",
                            
                            style={
                                "text-shadow": "2px 2px 5px rgba(0, 0, 0, 0.5)"
                            }
                        
                        ),
                        rx.text(
                            "Unlock a world of discovery in science, technology, and entertainment. The Image Analyzer lets you explore content-rich visuals with precision. Search for images across these themes, delve into their details, and ask AI-powered questions about each result. But it doesn’t stop there—generate insightful metadata, and create descriptive summaries with cutting-edge computer vision. Let your curiosity lead the way and redefine how you interact with images!",
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
                        rx.heading("Instructions for the 🖼 Image Analyzer",paddingX='1vw'),
                        rx.unordered_list(
                            rx.list_item(rx.text("Select Your Preferred Topic:",weight="bold"),rx.text("Begin by selecting the topic of your interest—be it science, technology, or another field relevant to your needs. This helps personalize your search and focuses on the content most relevant to you.")),
                            rx.list_item(rx.text("Load the Content:",weight="bold"),rx.text("Click the 'load content' button to load articles from scientific publications, technology showcases, or other relevant sources. The system will scan through these documents to extract images.")),
                            rx.list_item(rx.text("Choose Your Preferred Article:",weight="bold"),rx.text("Once the article is uploaded, select the article that interests you the most. The system will analyze the content and extract relevant images from the chosen article.")),
                            rx.list_item(rx.text("Interactive Image Selection:",weight="bold"),rx.text("A dynamic, interactive list of extracted images will appear. Browse through these images and select the ones that capture your attention or are relevant to your inquiry.")),
                            rx.list_item(rx.text("Ask Questions About the Images:",weight="bold"),rx.text("Once an image is selected, use the AI-driven interface to ask questions about it. The Image Analyzer will provide detailed insights, visual context, and descriptive summaries based on advanced computer vision.")),
                            rx.list_item(rx.text("Repeat for New Topics:",weight="bold"),rx.text("For each new topic or article, repeat the process—select the topic, upload the article, extract images, and explore. The system ensures seamless interaction, letting you dive deeper into each area of interest effortlessly.")),
                            paddingX='2vw',
                            paddingY="1vh"
                            

                        ),
                        rx.text("Let your exploration begin and unlock a new way to interact with visual content!",paddingX='1vw'),
                        
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
                                value=StateImgAnalyzer.topic,
                                placeholder="Write the topic to search",
                                on_change=StateImgAnalyzer.update_topic_values, 
                                
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
                                on_click=StateImgAnalyzer.load_articles_action,
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
                                StateImgAnalyzer.message_text,
                                color="red",
                                font_family="Times New Roman",
                                font_size="18px",
                                weight="bold",
                                padding_bottom="2vh",
                                display=rx.cond(StateImgAnalyzer.message_status,"block","none")
                                
                            ),
                        ),    
                        rx.center(
                            rx.fragment(
                                rx.select.root(
                                    rx.select.trigger(color_scheme='blue',variant='soft', placeholder="Select an article"),
                                    rx.select.content(
                                        rx.select.group(
                                            rx.foreach(
                                                StateImgAnalyzer.articles_titles,
                                                lambda x: rx.select.item(
                                                    x, value=x
                                                ),
                                            )
                                        ),
                                        color_scheme='amber',
                                        variant='solid'
                                    ),
                                    value=StateImgAnalyzer.article_selector,
                                    on_change=StateImgAnalyzer.update_selector_article,
                                    size='3'
                                
    ,
                                )                       
                            )
                        )    
                    ),
                    rx.box(
                        
                        rx.heading(
                            StateImgAnalyzer.title,
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
                        display=rx.cond(StateImgAnalyzer.show_title,"block","none")
                  
                    ),
                    
                    
                    rx.fragment(
                            rx.select.root(
                                rx.select.trigger(color_scheme='blue',variant='soft', placeholder="Select an image"),
                                rx.select.content(
                                    rx.select.group(
                                        rx.foreach(
                                            StateImgAnalyzer.images_article,
                                            lambda x: rx.select.item(
                                                x, value=x
                                            ),
                                        )
                                    ),
                                    color_scheme='amber',
                                    variant='solid'
                                ),
                                value=StateImgAnalyzer.image_selector,
                                on_change=StateImgAnalyzer.update_image_selector,
                                size='3'
                               
,
                            )                       
                    ),
                    
                    rx.image(
                    
                    src=StateImgAnalyzer.img,  # URL de la imagen
                    alt="Descripción de la imagen",
                    width="60%",  # Ancho de la imagen
                    height="40vh",   # Altura ajustada automáticamente
                    align="center",
                    display=rx.cond(StateImgAnalyzer.show_image,"block","none")
                    ),
                    rx.box(
                        rx.center(
                            rx.heading(
                            "Chat with the image",
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

