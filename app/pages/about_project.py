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
                    
                    src="https://upload.wikimedia.org/wikipedia/commons/1/1f/Ucatolica2.jpg",  # URL de la imagen
                    alt="Descripción de la imagen",
                    width="10vw",  # Ancho de la imagen
                    height="auto",   # Altura ajustada automáticamente
                    
                ),
                rx.heading(
                    'NOMBRE DEL PROYECTO IMAGINEPROJECT',
                                        
                    weight="medium",
                    high_contrast=True,
                    font_family="Times New Roman",
                    font_size="31px",
                    padding_left="5vw",
                    margin_top="2.5vh"
                   
                ),     
               
                
                padding_left="15vw",
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
                            "ACERCA DEL PROYECTO",
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
                        
                        rx.text(
                            "Text",
                            text_align="justify",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='8px',
                            weight="regular",
                        
                        ),
                    direction="column",
                    height="100%",
                    background_color="#E3E4E5",
                    width="90%",
                    paddingY='3vh'
                    
                    ),
                    rx.image(
                    
                    src="/new_society.jpg",  # URL de la imagen
                    alt="Descripción de la imagen",
                    width="50%",  # Ancho de la imagen
                    height="30vh",   # Altura ajustada automáticamente
                    align="center",
                    ),
                    rx.box(
                        
                        rx.text(
                            "Other text",
                            text_align="justify",
                            font_family="Times New Roman",
                            font_size="24px",
                            paddingX='8px',
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