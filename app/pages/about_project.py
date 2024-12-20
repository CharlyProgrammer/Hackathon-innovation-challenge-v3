import reflex as rx 

def page_content():
    with open('./assets/just-proy.txt','r',encoding="utf-8") as file:
        text=file.read()
    return text    
        
def about_project():
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
        rx.center(
            rx.box(
                rx.center(
                    rx.box(
                        
                        rx.heading(
                            "ABOUT THE PROPOSED PROJECT ",
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
                    
                    ),
                    rx.box(
                        rx.heading(
                            "Unleashing the Power of AI for Smarter Interactions with Information",
                            weight="bold",
                            paddingX="2vw"
                        ),
                        rx.text(
                            "In a world where knowledge is vast and opportunities are endless, AI-Bits brings together the transformative potential of Artificial Intelligence (AI) and the foundational essence of data, or 'bits' The name reflects our mission: leveraging AI to unlock the 'bits' of information that matter most—making them accessible, interactive, and meaningful.",
                            text_align="justify",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='2vw',
                            weight="regular",
                                              
                        ),
                        rx.text(
                            "Why AI-Bits?",
                            text_align="justify",
                            weight="bold",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='2vw',
                           
                                              
                        ),
                        rx.text(
                            "AI-Bits is more than just a tool; it’s a revolution in how we interact with information online. Designed to seamlessly combine AI Search and Retrieval Augmented Generation (RAG), it redefines relevance and personalization, catering to context and intent like never before. With AI-Bits, we harness the power of cutting-edge AI technologies to:",
                            text_align="justify",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='2vw',
                            weight="regular",
                                              
                        ),
                        rx.unordered_list(
                                    rx.list_item(rx.text("Chat with Internet Images: ",weight="bold"),rx.text("Explore ideas visually by retrieving and interacting with images from the web.",font_family="Times New Roman",font_size="24px")),
                                    rx.list_item(rx.text("Chat with Websites: ",weight="bold"),rx.text("Dive deep into the context of reliable sites, gaining insights with precision and clarity.",font_family="Times New Roman",font_size="24px")),
                                    rx.list_item(rx.text("Chat with Documents: ",weight="bold"),rx.text("Upload and interact with documents to uncover key information in seconds.",font_family="Times New Roman",font_size="24px")),
                                    rx.list_item(rx.text("Chat with Videos: ",weight="bold"),rx.text("Extract meaningful content from videos, breaking them down into digestible, actionable insights.",font_family="Times New Roman",font_size="24px")),
                                    paddingX='2vw',
                        ),
                        
                    direction="column",
                    height="100%",
                    background_color="#E3E4E5",
                    width="90%",
                    paddingY='3vh'
                    
                    ),
                    rx.image(
                    
                    src="https://www.eiopa.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2022-03/ai-big-data.jpg?itok=3O6ERwTi",  # URL de la imagen
                    alt="/about.png",
                    width="90%",  # Ancho de la imagen
                    height="40vh",   # Altura ajustada automáticamente
                    align="center",
                    ),
                    rx.box(
                        
                         rx.text(
                            "The Core Features:",
                            text_align="justify",
                            weight="bold",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='2vw',
                           
                                              
                        ),
                        rx.text(
                            "AI-Bits empowers users through four groundbreaking functionalities, focused on science and technology:",
                            text_align="justify",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='2vw',
                            weight="regular",
                                              
                        ),
                        rx.unordered_list(
                                    rx.list_item(rx.text("Provide richer, interactive search experiences.",font_family="Times New Roman",font_size="24px")),
                                    rx.list_item(rx.text("Bridge the gap between knowledge and accessibility.",font_family="Times New Roman",font_size="24px")),
                                    rx.list_item(rx.text("Enhance the way we understand and utilize online content.",font_family="Times New Roman",font_size="24px")),
                                    paddingX='2vw',
                        ),
                        rx.text(
                            "Our Vision",
                            text_align="justify",
                            weight="bold",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='2vw',
                           
                                              
                        ),
                         rx.text.quote(
                            "The web unlocks knowledge, and AI opens doors to endless opportunities and true accessibility.",
                            text_align="justify",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='2vw',
                            weight="regular",
                                              
                        ),
                        rx.text(
                            "This guiding principle drives AI-Bits to be a game-changer in online information interaction. Join us in transforming how we connect with the digital world. With AI-Bits, the possibilities are endless, the experiences richer, and the information more accessible than ever.",
                            text_align="justify",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='2vw',
                            weight="regular",
                                              
                        ),
                    direction="column",
                    height="100%",
                    background_color="#E3E4E5",
                    width="90%",
                    paddingY='3vh'
                    
                    ),
                    spacing='40px',
                    direction="column",
                    paddingY='3vh'
                ), 
                
                direction="column",
                height="100%",
                background_color="white",
                width="80%",
            
            ),
            
            background_color="#bdbdbd",
            width="100%",
            height='100%'
            
        ),    
        
    height="100%",
    width="100%",
    )