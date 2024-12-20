import reflex as rx 
class StateTeam(rx.State):
   
    data_cards:list[list]=[
            [1,"Carlos Maldonado","/video.jpg","[Member]"],
            [2,"Charlie","/website_analyzer.jpg","[Member]"],
                
            
        ]

def create_cards(data_cards:list[tuple]):
        
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
                    
                    rx.icon("user"),
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
                
def about_team():
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
                            "THE DEVELOPERS",
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
                        
                         rx.grid(
                            rx.foreach(
                               StateTeam.data_cards,
                               create_cards,
                            ),
                            columns="2",
                            spacing="8",
                            width="50vw",
                            paddingX="5vw",
                            overflow_x="auto",
                        )
                    
                    ),
                    
                    
                    spacing='40px',
                    direction="column",
                    paddingY='3vh'
                ), 
                
                direction="column",
                height="100%",
                background_image="url('https://www.restoringthewells.org/wp-content/uploads/2016/02/dreamstime_m_53527973.jpg')",
                width="80%",
            
            ),
            
            background_color="#bdbdbd",
            width="100%",
            height='85vh'
            
        ),    
        
    height="100%",
    width="100%",
    )