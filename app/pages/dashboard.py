import reflex as rx 
#from app.database.connection import database

class StateDashboard(rx.State):
    status_button_1:bool=True
    status_button_2:bool=True
    status_button_3:bool=True
    status_button_4:bool=True
    status_button_5:bool=True
    user:str=""
    data_cards:list[list]=[
        [1,"🚀 Unleash the Power of Video Exploration!","/video.jpg","Transform how you interact with video content using the Video Analyzer. Search any topic, browse curated video titles, and dive into selected content with transcriptions and AI-driven Q&A. Experience hands-free interaction with voice input and audio output, redefining accessibility. Whether you're learning, researching, or just exploring, the Video Analyzer lets you unlock the secrets within every frame. Dive into discovery today—where no question is out of reach and every answer awaits!",status_button_1,'/home/dashboard/video-analyzer'],
        [2,"Tools for webpage analysis","/website_analyzer.jpg","Unlock a world of knowledge at your fingertips with the Web Analyzer. Dive into relevant content tailored to your interests—be it science, technology, or any field you desire. Select articles that inspire curiosity, explore them with our interactive chat tool, and ask questions to enrich your learning experience. Whether you're seeking insights, deepening your understanding, or exploring new frontiers, the Web Analyzer empowers you to interact with information in a more engaging and meaningful way. Start your journey of discovery today!",status_button_2,'/home/dashboard/web-analyzer'],
        [3,"Tools for image analysis","/image_analyzer.jpg","Unlock a world of discovery in science, technology, and entertainment. The Image Analyzer lets you explore content-rich visuals with precision. Search for images across these themes, delve into their details, and ask AI-powered questions about each result. But it doesn’t stop there—generate insightful metadata, and create descriptive summaries with cutting-edge computer vision. Let your curiosity lead the way and redefine how you interact with images!",status_button_3,'/home/dashboard/image-analyzer'],
        [4,"Chat with documents","/chatbot.jpg","Description 4",status_button_4,'/home/dashboard'],
        
        
    ]
    

       
   
   
            

def create_service(data_cards:list[tuple]):
        
        return rx.card(
            rx.center(
                rx.card(
                    rx.heading(
                       data_cards[0]
                    ),
                    width="fit-content",
                    height="auto",
                    background="orange"
                ),
            ),    
            rx.center(
                rx.hstack(
                    
                    rx.icon("school"),
                    rx.heading(
                        data_cards[1],
                        font_family="Console",
                        font_size="24px",
                        weight="bold",
                    ),
                    _hover={
                        "color": "#EFB810"  # Cambia el color del texto al pasar el cursor
                    }
                ),
                rx.image(
                    src=data_cards[2],
                    height="20vh",  # Altura de la ventana
                    width="12vw", 
                    style={
                                        
                        "border-radius": "50%",  
                        "border": "8px solid #c3834d",  
                    }
                    
                ),
                
                rx.card(
                    data_cards[3],
                    width="80%",
                    height="fit-content",
                    text_align="justify",
                   
                ),
                rx.button(
                    "Open",
                    display=rx.cond(data_cards[4],'block','none'),
                    on_click=lambda: rx.redirect(data_cards[5]),
                    cursor="pointer",
                    _hover={
                        "color": "#FFD700",  # Cambia el color del texto al pasar el cursor
                       
                    }
                    
                ),
                direction="column",
                spacing="1.5vh",
                
            ),
                
            width="100%",
            height="fit-content",
            background="#CBB799",
            style={
                    "border-radius": "30px",  
                    "border": "4px solid #009929",  
            }
        )   
        
    

def aplications_dashboard():
     
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
                    on_click=lambda: rx.redirect("/home")
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
        
        rx.box(
            
            rx.flex(
                    rx.box(
                        
                        rx.heading(
                            f"Welcome to Your AI-Powered Interactive Dashboard!",
                            align="center",
                            font_family="Console",
                            font_size="38px",
                            weight="bold",
                            
                            style={
                                "text-shadow": "2px 2px 5px rgba(0, 0, 0, 0.5)"
                            }
                            
                        
                        ),
                    style={
                        "border-radius": "100px"
                    },    
                    direction="column",
                    height="100%",
                    background_color="white",
                    width="50%",
                    paddingY='3vh',
                    
                    
                    
                    ),
                    
                    rx.hstack(
                        
                        rx.card(
                            rx.center(
                                rx.heading(
                                    "Why This Dashboard Stands Out?",
                                     font_family="Console",
                                     font_size="21px",
                                     weight="bold",
                                    
                                     
                            
                                ),
                                rx.separator(
                                    border_width="2px",  # Grosor del separador
                                    border_color="#0cb7f2",  # Color del separador
                                     # Margen alrededor del separador
                                ),
                                rx.text(
                                   "Each card on the dashboard represents a powerful functionality that empowers you to extract insights, interact with content, and unlock the true potential of modern technology. Whether you're a researcher, enthusiast, or industry leader, this app delivers:",
                                   paddingX="1vw",
                                   style={'text-align': 'justify'} 
                                ),
                                rx.unordered_list(
                                    rx.list_item(rx.text("Contextual Understanding:",weight="bold"),rx.text("Enhanced search precision by grasping user intent.")),
                                    rx.list_item(rx.text("Seamless Integration:",weight="bold"),rx.text("Combining Natural Language Processing (NLP), Computer Vision, and more to provide intuitive interactions.")),
                                    rx.list_item(rx.text("Personalization at Scale:",weight="bold"),rx.text("Tailored experiences that anticipate your needs."))
                                ),
                                direction='column',
                                spacing="1vh",
                                style={
                                     "border-radius": "100px",
                                     
                                }
                                
                            ),
                                 
                           
                            width="20vw",
                            height="50vh",
                            style={
                                     "border-radius": "50px",
                            },
                            background="#b5b5b5"
                        ),
                        rx.grid(
                            rx.foreach(
                                StateDashboard.data_cards,
                                create_service,
                            ),
                            columns="2",
                            spacing="8",
                            width="60vw",
                            paddingX="5vw",
                            overflow_x="auto",
                        ),
                        
                   
                        
                    ),
                    
                      
                   
                    spacing='40px',
                    direction="column",
                    padding='3vh'
                ),
            
            background_color="#E8DFCC",
            width="100%",
            height='100%'
            
        ),    
        
    height="100%",
    width="100%",
    
    
    )