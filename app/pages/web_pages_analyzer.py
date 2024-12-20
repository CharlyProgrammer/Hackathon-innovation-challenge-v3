import reflex as rx 
from app.scripts_for_rag.scrap_data import extract_web_data
from app.styles import style_copilot
from app.scripts_for_rag.calls_models import model_completion
from app.scripts_for_rag.call_voice_models import voice_manager
import time
import os
class StateWebAnalyzer(rx.State):
    title: str=""
    article_highlight:str=""
    article_text: str=""
    topic: str=""
    message_text:str=""
    response:str=""
    historial: list[tuple[str, str]]
    article_selector:str=""
    chat_field: str=""
    show_title: bool=False
    show_text_article: bool=False
    send_read_status: bool=False
    send_chat_status:bool=False
    voice_status: bool=False
    message_status: bool=False
    loading_state: bool=False
    audio_loading_state: bool=False
    show_audio: bool=False
    articles_urls:list[str]=[]
    articles_titles: list[str]=[]
      
    @rx.event
            
    def update_selector_article(self,value:str):
        self.article_selector=value
        self.title=self.article_selector
        self.show_title=True
               
        obj=extract_web_data()
        
        for idx,article in enumerate(self.articles_titles):
            if self.article_selector==article:
                
                url=self.articles_urls[idx]
                data=obj.get_article(url)
                self.article_highlight=data["highlight"]
                self.article_text=data["content"]
                self.show_text_article=True
                self.send_chat_status=True
                self.send_read_status=True
                self.show_audio=False
                
    def change_mic_status(self):
        self.voice_status=True                
    def update_chat_field(self,value):
        self.chat_field=value    
    def init_loading(self):
        self.loading_state=True
    def init_audio_loading(self):
        self.show_audio=False
        self.audio_loading_state=True
    def save_chat(self):
        try:
            answer=run_conversation(self.chat_field,self.article_text)
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
                answer=run_conversation(voice,self.article_text)
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
            self.article_selector=""
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
            self.article_selector=""
            self.articles_urls=[]
            self.articles_titles=[]
            self.topic=""
            self.message_text="<!> Error, topic field cannot be empty"
            self.message_status=True
            self.send_chat_status=False
            self.send_read_status=False
                            
    
    
    def back_action(self):
       
        self.article_selector=""
        self.articles_urls=[]
        self.articles_titles=[]
        self.historial=[]
        self.title=""
        self.topic=""
        self.show_audio=False
        self.show_text_article=False
        self.send_chat_status=False
        self.send_read_status=False
        self.voice_status=False
        if os.path.isfile("./uploaded_files/response.mp3"):
        
            os.remove("./uploaded_files/response.mp3")
        return rx.redirect("/home/dashboard")

def run_conversation(user_prompt,context):
    #obj_llm_completion=model_completion("LLAMA_KEY","LLAMA_MODEL","OPENAI_KEY","OPENAI_MODEL","OPENAI_ENDPOINT")
    
    obj_llm_completion=model_completion(key_model_oa="OPENAI_KEY",endpoint_oa="OPENAI_ENDPOINT",model_version_oa="OPENAI_MODEL")
    messages=[{"role": "user","content": f"Based in the next context:{context}, answer the next query:{user_prompt}"}]
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
            StateWebAnalyzer.historial,
            lambda messages: qa(messages[0], messages[1]),
        ),
        width="40vw"
        
         
    )

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=StateWebAnalyzer.chat_field,
            placeholder="Make a question",
            on_change=StateWebAnalyzer.update_chat_field, 
            style=style_copilot.input_style,
            background_color="white",
            height="4vh"
        ),
        rx.button(
            "Send",
            on_click=lambda:[StateWebAnalyzer.init_loading,StateWebAnalyzer.save_chat],
            style=style_copilot.button_style,
            height="4vh",
            
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            loading=StateWebAnalyzer.loading_state,
            display=rx.cond(StateWebAnalyzer.send_chat_status,"block","none")
        ),
        rx.button(
            rx.icon("mic"),
            background_color=rx.cond(StateWebAnalyzer.voice_status,"red","blue"),
            on_click=lambda:[StateWebAnalyzer.change_mic_status,StateWebAnalyzer.save_voice],
            style=style_copilot.button_style,
            height="4vh",
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            
            display=rx.cond(StateWebAnalyzer.send_chat_status,"block","none")
        ),
        rx.button(
            "Read",
            on_click=lambda:[StateWebAnalyzer.init_audio_loading,StateWebAnalyzer.send_text_read],
            style=style_copilot.button_style,
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            height="4vh",
            loading=StateWebAnalyzer.audio_loading_state,
            display=rx.cond(StateWebAnalyzer.send_read_status,"block","none")
        ),
        rx.box(
            rx.cond(
                StateWebAnalyzer.show_audio,
                rx.audio(
                    url=rx.get_upload_url("response.mp3"),
                    width="400px",
                    height="32px",
           

                ),
                rx.box()
            )
        )
    )





        
def web_analyzer_page():
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
                    on_click=StateWebAnalyzer.back_action 
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
                            "Welcome to the Web analyzer",
                            align="center",
                            font_family="Console",
                            font_size="38px",
                            weight="bold",
                            
                            style={
                                "text-shadow": "2px 2px 5px rgba(0, 0, 0, 0.5)"
                            }
                        
                        ),
                        rx.text(
                            "Unlock a world of knowledge at your fingertips with the Web Analyzer. Dive into relevant content tailored to your interests—be it science, technology, or any field you desire. Select articles that inspire curiosity, explore them with our interactive chat tool, and ask questions to enrich your learning experience. Whether you're seeking insights, deepening your understanding, or exploring new frontiers, the Web Analyzer empowers you to interact with information in a more engaging and meaningful way. Start your journey of discovery today!",
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
                        rx.heading("Instructions for the 🌐 Web Analyzer",paddingX='1vw'),
                        rx.unordered_list(
                            rx.list_item(rx.text("Enter Your Preferred Topic: ",weight="bold"),rx.text("Start by typing the topic of your interest into the Topic field. This will help tailor your search and focus on content relevant to your needs.")),
                            rx.list_item(rx.text("Load the Content: ",weight="bold"),rx.text("Click the 'Load Content' button to retrieve search results related to your chosen topic. The system will gather and display relevant articles based on your input.")),
                            rx.list_item(rx.text("Choose Your Preferred Article: ",weight="bold"),rx.text("Once the content is loaded, a list of relevant articles will appear. Select the one that interests you the most to dive deeper into its content.")),
                            rx.list_item(rx.text("Activate the Chat with the Article: ",weight="bold"),rx.text("Upon selecting an article, the system will activate a chat interface or a copilot tool for that specific article. Use it to ask questions, explore deeper insights, and enhance your understanding of the content.")),
                            rx.list_item(rx.text("Ask Questions & Explore: ",weight="bold"),rx.text("View the article content, engage with the chat interface, and ask questions to gain detailed explanations, summaries, or any additional information you seek.")),
                            rx.list_item(rx.text("Repeat for New Topics: ",weight="bold"),rx.text("For each new topic, repeat the process—select a new topic, retrieve and select articles, and explore using the chat feature. Each session resets, ensuring fresh interactions with every query.")),
                            rx.list_item(rx.text("Inputs: ",weight="bold"),rx.text("For each new prompt or query, our system can process either a text input in the chat or an audio input through a microphone (just push the button and speak when it is in red)")),
                            rx.list_item(rx.text("Outputs: ",weight="bold"),rx.text("Like in the case of the inputs, our system can give either a text output in the chat or an audio output through a speaker element (just push the button 'READ' and wait it is ready, but sometimes it can take a few minutes)")),
                            paddingX='2vw',
                            paddingY="1vh"
                            

                        ),
                        rx.text("Let your exploration begin and unlock a new way to interact with your favorite content!",paddingX='1vw'),
                        
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
                                value=StateWebAnalyzer.topic,
                                placeholder="Write the topic to search",
                                on_change=StateWebAnalyzer.update_topic_values, 
                                
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
                                on_click=StateWebAnalyzer.load_articles_action,
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
                                StateWebAnalyzer.message_text,
                                color="red",
                                font_family="Times New Roman",
                                font_size="18px",
                                weight="bold",
                                padding_bottom="2vh",
                                display=rx.cond(StateWebAnalyzer.message_status,"block","none")
                                
                            ),
                        ),    
                        rx.center(
                            rx.fragment(
                                rx.select.root(
                                    rx.select.trigger(color_scheme='blue',variant='soft', placeholder="Select an article"),
                                    rx.select.content(
                                        rx.select.group(
                                            rx.foreach(
                                                StateWebAnalyzer.articles_titles,
                                                lambda x: rx.select.item(
                                                    x, value=x
                                                ),
                                            )
                                        ),
                                        color_scheme='amber',
                                        variant='solid'
                                    ),
                                    value=StateWebAnalyzer.article_selector,
                                    on_change=StateWebAnalyzer.update_selector_article,
                                    size='3'
                                
    ,
                                )                       
                            )
                        )    
                    ),
                    rx.box(
                        
                        rx.heading(
                            StateWebAnalyzer.title,
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
                        display=rx.cond(StateWebAnalyzer.show_title,"block","none")
                  
                    ),
                    
                    
                   
                    
                    rx.box(
                        
                        rx.text(
                            StateWebAnalyzer.article_text,
                            align="center",
                            font_family="Console",
                            font_size="18px",
                            weight="normal",
                            style={'text-align': 'justify'} ,
                            paddingX="1vw"
                        
                        ),
                        direction="column",
                        height="fit-content",
                        background_color="#E3E4E5",
                        width="90%",
                        paddingY='3vh',
                        border_color="black",  # Color del borde
                        border_width="2px",
                        display=rx.cond(StateWebAnalyzer.show_text_article,"block","none")
                  
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

