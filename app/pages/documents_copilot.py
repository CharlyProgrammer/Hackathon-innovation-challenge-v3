import reflex as rx 
from app.styles import style_copilot
from app.scripts_for_rag.calls_models import model_completion
from app.scripts_for_rag.call_voice_models import voice_manager
import time
import os
class StateDocsAnalyzer(rx.State):
    title: str=""
    message_text:str=""
    response:str=""
    historial: list[tuple[str, str]]
    chat_field: str=""
    send_read_status: bool=False
    send_chat_status:bool=False
    voice_status: bool=False
    message_status: bool=False
    loading_state: bool=False
    audio_loading_state: bool=False
    show_audio: bool=False
    
      
    @rx.event
            
    
                
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
            answer=run_conversation(self.chat_field)
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
        
    
    def back_action(self):
       
       
        self.historial=[]
        self.show_audio=False
        self.send_chat_status=False
        self.send_read_status=False
        self.voice_status=False
        if os.path.isfile("./uploaded_files/response.mp3"):
        
            os.remove("./uploaded_files/response.mp3")
        return rx.redirect("/home/dashboard")

def run_conversation(user_prompt):
    #obj_llm_completion=model_completion("LLAMA_KEY","LLAMA_MODEL","OPENAI_KEY","OPENAI_MODEL","OPENAI_ENDPOINT")
    
    obj_llm_completion=model_completion(key_model_oa="OPENAI_KEY",endpoint_oa="OPENAI_ENDPOINT",model_version_oa="OPENAI_RAG_MODEL")
    messages=[{"role": "user","content": f"Based in the context, answer the next query:{user_prompt}"}]
    client=obj_llm_completion.init_model_openai()
    response=obj_llm_completion.generate_response_RAG_openai(client=client,messages=messages,temperature=0.8,max_tokens=800)
   
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
            StateDocsAnalyzer.historial,
            lambda messages: qa(messages[0], messages[1]),
        ),
        width="40vw"
        
         
    )

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=StateDocsAnalyzer.chat_field,
            placeholder="Make a question",
            on_change=StateDocsAnalyzer.update_chat_field, 
            style=style_copilot.input_style,
            background_color="white",
            height="4vh"
        ),
        rx.button(
            "Send",
            on_click=lambda:[StateDocsAnalyzer.init_loading,StateDocsAnalyzer.save_chat],
            style=style_copilot.button_style,
            height="4vh",
            
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            loading=StateDocsAnalyzer.loading_state,
            
        ),
        rx.button(
            rx.icon("mic"),
            background_color=rx.cond(StateDocsAnalyzer.voice_status,"red","blue"),
            on_click=lambda:[StateDocsAnalyzer.change_mic_status,StateDocsAnalyzer.save_voice],
            style=style_copilot.button_style,
            height="4vh",
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            
            
        ),
        rx.button(
            "Read",
            on_click=lambda:[StateDocsAnalyzer.init_audio_loading,StateDocsAnalyzer.send_text_read],
            style=style_copilot.button_style,
            cursor="pointer",
            _hover={
                "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
            },
            height="4vh",
            loading=StateDocsAnalyzer.audio_loading_state,
           
        ),
        rx.box(
            rx.cond(
                StateDocsAnalyzer.show_audio,
                rx.audio(
                    url=rx.get_upload_url("response.mp3"),
                    width="400px",
                    height="32px",
           

                ),
                rx.box()
            )
        )
    )





        
def documents_chat_page():
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
                    on_click=StateDocsAnalyzer.back_action 
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
                            "Welcome to the Document analyzer",
                            align="center",
                            font_family="Console",
                            font_size="38px",
                            weight="bold",
                            
                            style={
                                "text-shadow": "2px 2px 5px rgba(0, 0, 0, 0.5)"
                            }
                        
                        ),
                        rx.text(
                            "Unlock the full potential of your documents with 📄 Document Analyzer, the ultimate tool in AI-BITS. Powered by Retrieval Augmented Generation (RAG) and advanced generative AI, this groundbreaking feature transforms the way you access, explore, and interact with information. Whether it’s PDFs, JSON files, or even slides, the Document Analyzer bridges the gap between data and understanding, bringing clarity to complex content.",
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
                        rx.text(
                            "Imagine a world where your documents answer your questions directly, adapting to your needs in real time. Ask your queries through text or voice—the choice is yours. With responses delivered in precise text or engaging audio via an integrated player, Document Analyzer ensures information is accessible, no matter your preference.",
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
                        rx.text(
                            "Gone are the days of endless scrolling or fruitless searches. With Azure AI Search powering its database and AI enhancing its insights, this tool redefines accessibility. From students unraveling research to professionals diving into dense reports, Document Analyzer is your key to smarter, more interactive, and deeply personalized data exploration.",
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
                        rx.heading("Instructions for the 📄 Documents Analyzer",paddingX='1vw'),
                        rx.unordered_list(
                            rx.list_item(rx.text("Explore Boundless Knowledge: ",weight="bold"),rx.text("Step into the future of information retrieval! AI-BITS harnesses the power of Retrieval Augmented Generation (RAG) through Azure AI Search and advanced generative AI models, offering unparalleled interaction with documents.")),
                            rx.list_item(rx.text("Seamless Input Options: ",weight="bold"),rx.text("Whether you're typing or speaking, AI-BITS adapts to you. Ask questions in the chat using text input or use your microphone to interact with the system through voice commands.")),
                            rx.list_item(rx.text("Comprehensive Output Choices: ",weight="bold"),rx.text("Receive answers in real-time through chat in text format or elevate your experience with audio responses. Simply press the 'Read' button, and the system will transform the response into audio, available through an integrated player.")),
                            rx.list_item(rx.text("Access a Rich Database: ",weight="bold"),rx.text("Leverage a powerful database of documents, including PDFs and JSON files, meticulously curated to deliver the most accurate and relevant results to your queries.")),
                            rx.list_item(rx.text("Unlock Advanced AI-Powered Insights: ",weight="bold"),rx.text("AI-BITS understands context and intent, providing personalized, precise answers to your questions. Whether you're researching, learning, or solving complex problems, it empowers you to uncover insights like never before.")),
                            rx.list_item(rx.text("Discover New Possibilities: ",weight="bold"),rx.text("With AI-BITS, interaction with data transcends traditional methods. By combining cutting-edge AI search with generative models, this tool redefines how we access and engage with information online.")),
                            rx.list_item(rx.text("Inputs: ",weight="bold"),rx.text("For each new prompt or query, our system can process either a text input in the chat or an audio input through a microphone (just push the button and speak when it is in red)")),
                            rx.list_item(rx.text("Outputs: ",weight="bold"),rx.text("Like in the case of the inputs, our system can give either a text output in the chat or an audio output through a speaker element (just push the button 'READ' and wait it is ready, but sometimes it can take a few minutes)")),
                            paddingX='2vw',
                            paddingY="1vh"
                            

                        ),
                        rx.text("Let your exploration begin and unlock a new way to interact with your favorite content!",paddingX='1vw'),
                        rx.text("💡 Your Key to Smarter, Interactive Information Retrieval",weight="bold",paddingX='1vw',paddingY="1vh"),
                        rx.text("AI-BITS isn't just a tool; it's a revolution in how you interact with data. From text to voice, it creates a seamless, personalized experience tailored to your needs.",paddingX='1vw'),
                        
                    direction="column",
                    height="100%",
                    background_color="#E3E4E5",
                    width="90%",
                    paddingY='3vh',
                                       
                    ),
                    
                                 
                    rx.box(
                        rx.center(
                            rx.heading(
                            "Chat with documents",
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

