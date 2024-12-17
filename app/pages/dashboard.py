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
        [1,"TITLE 1","/func-1.png","Description 1",status_button_1,'/account/user/autoeval-platform/generator'],
        [2,"TITLE 2","/examen_virtual.jpg","Description 2",status_button_2,'/account/user/autoeval-platform/test-in-platform'],
        [3,"TITLE 3","/soluciones.jpg","Description 3",status_button_3,'/account/user/autoeval-platform/upload-answer-system'],
        [4,"TITLE 4","/reporte.png","Description 4",status_button_4,'/account/user/autoeval-platform/test-reports'],
        [5,"TITLE 5","/chatbot.jpg","[Copilot] Description 5",status_button_5,'/account/user/autoeval-platform/assistant']
    
        
    ]
    data_time_line: list[tuple]=[]    
        
    def update_test_services(self):
        
        self.data_cards[0][4]=False
        self.data_cards[1][4]=True
        
       
    def test_taked(self):
        self.data_cards[0][4]=False
        self.data_cards[1][4]=False
        self.data_cards[2][4]=False
    
   
    def update_status_platform(self):
        self.data_cards[0][4]=True
        self.data_cards[1][4]=False
        self.data_cards[2][4]=True
        self.data_cards[3][4]=True
        self.data_cards[4][4]=True
    
   
            
def create_time_line(data:list[tuple]):
    return rx.box(
                rx.text(
                    data[0],
                    font_family="Console",
                    font_size="18px",
                    weight="bold"
                ),
                rx.card(
                   data[1],
                ),
                width="90%",
                paddingX="1vw",                          
                
                
           )

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
                        font_size="18px",
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
                        "border": "4px solid #c3834d",  
                    }
                    
                ),
                
                rx.card(
                    data_cards[3],
                    width="80%",
                    height="fit-content",
                    text_align="justify",
                   
                ),
                rx.button(
                    "Ingresar",
                    display=rx.cond(data_cards[4],'block','none'),
                    on_click=lambda: rx.redirect(data_cards[5]),
                    cursor="pointer",
                    _hover={
                        "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
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
        
        rx.box(
            
            rx.flex(
                    rx.box(
                        
                        rx.heading(
                            f"Dashboard of utilities",
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
                    width="35%",
                    paddingY='3vh',
                    
                    
                    
                    ),
                    
                    rx.hstack(
                        
                        rx.card(
                            rx.center(
                                rx.heading(
                                    "LINEA DEL TIEMPO",
                                     font_family="Console",
                                     font_size="21px",
                                     weight="bold",
                                    
                                     
                            
                                ),
                                rx.separator(
                                    border_width="2px",  # Grosor del separador
                                    border_color="#0cb7f2",  # Color del separador
                                     # Margen alrededor del separador
                                ),
                                
                                direction='column',
                                spacing="1vh",
                                style={
                                     "border-radius": "100px",
                                     
                                }
                                
                            ),
                            rx.box(
                                
                                rx.foreach(
                                    StateDashboard.data_time_line,
                                    create_time_line
                                
                                ),
                                height="40vh",
                                paddingY="1vh",    
                                overflow_y="auto" 
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
                            columns="3",
                            spacing="8",
                            width="70vw",
                            paddingX="5vw",
                            overflow_x="auto",
                        )
                   
                        
                    ),
                    
                      
                   
                    spacing='40px',
                    direction="column",
                    padding='3vh'
                ),
            
            background_image="url('https://150000629.v2.pressablecdn.com/wp-content/uploads/2021/01/learn--scaled.jpg')",
            width="100%",
            height='100%'
            
        ),    
        
    height="100%",
    width="100%",
    
    
    )