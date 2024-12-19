import reflex as rx
class StateHome(rx.State):
    color_heading:str="black"
    def color_action(self):
        self.color_heading="white"
def home() -> rx.Component:
    # Welcome Page (Index)
    return rx.box(
        rx.color_mode.button(position="top-right"),
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
            rx.center(
                               
               
                rx.menu.root(
                    rx.menu.trigger(
                        rx.heading(
                            "Learn more",
                            color="white",
                            font_family="Arial",
                            font_size="20px",
                            cursor="pointer",
                            _hover={
                                "color": "cyan"  # Cambia el color del texto al pasar el cursor
                            },
                            
                        ),
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            rx.icon('book-open'),
                            "About the project",
                            on_click=lambda: rx.redirect('/home/about-project'),
                            style={ "font-family": "Console",
                                    "font-size": "20px",
                                    "font-weight": "normal",
                                    "cursor": "pointer"  # Cambiar el cursor al pasar el mouse
                                  }
                            ),
                        rx.menu.item(
                            rx.icon('users'),
                            "About the developers",
                            on_click=lambda: rx.redirect('/home/about-team'),
                            style={ "font-family": "Console",
                                    "font-size": "20px",
                                    "font-weight": "normal",
                                    "cursor": "pointer"  # Cambiar el cursor al pasar el mouse
                                  }
                            ),
                        rx.menu.separator(),
                        rx.menu.item(
                            rx.icon('video'),
                            "Presentation", 
                            
                            on_click=lambda:rx.redirect("https://www.youtube.com/",external=True),
                            style={ "font-family": "Console",
                                    "font-size": "20px",
                                    "font-weight": "normal",
                                    "cursor": "pointer"  # Cambiar el cursor al pasar el mouse
                                  }
                        ),
                         style= {
                            "position": "absolute",
                            'width':'250px',
                            'height':'auto',
                            "right": "1vw",  # 10% de la altura de la ventana
                            
                    
                        }
                       
                        
                    )    
                ),
                rx.heading(
                    "Enter to the dashboard",
                    color="white",
                    font_family="Arial",
                    font_size="20px",
                    cursor="pointer",
                    _hover={
                        "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
                    },
                    on_click=lambda: rx.redirect('/home/dashboard'),
                    #display= ComponentState.visibility_access
                ),
                spacing='100px',
                direction="row",
            ),
            
            display="flex", 
            alignItems="center",
            justifyContent="right",
            background_color=StateHome.color_heading,
            height="4vh",
            min_height='50px',
            max_height='100px',
            paddingX='15vw'
        ),
        rx.center(
            
            rx.box(
                rx.image(
                    src="/phrase.png",  # Ruta de la imagen
                    alt="Descripción de la imagen",
                    width="100%",  # Ancho de la imagen
                    height="50vh",   # Altura ajustada automáticamente
                    
                ),
                rx.image(
                    src="/divisor.png",  # Ruta de la imagen
                    alt="Divisor",
                    width="100%",  # Ancho de la imagen
                    height="50px",   # Altura ajustada automáticamente
                    
                ),
                rx.image(
                    src="/phrase.png",  # Ruta de la imagen
                    alt="Descripción de la imagen",
                    width="100%",  # Ancho de la imagen
                    height="50vh",   # Altura ajustada automáticamente
                    
                ),
                rx.image(
                    src="/divisor.png",  # Ruta de la imagen
                    alt="Divisor",
                    width="100%",  # Ancho de la imagen
                    height="50px",   # Altura ajustada automáticamente
                    
                ),
                rx.image(
                    src="/home-beneficios.png",  # Ruta de la imagen
                    alt="Descripción de la imagen",
                    width="100%",  # Ancho de la imagen
                    height="50vh",   # Altura ajustada automáticamente
                    
                ),
                rx.image(
                    src="/divisor.png",  # Ruta de la imagen
                    alt="Divisor",
                    width="100%",  # Ancho de la imagen
                    height="50px",   # Altura ajustada automáticamente
                    
                ),
                rx.image(
                    src="/architecture.png",  # Ruta de la imagen
                    alt="Descripción de la imagen",
                    width="100%",  # Ancho de la imagen
                    height="50vh",   # Altura ajustada automáticamente
                    
                ),
                rx.image(
                    src="/divisor.png",  # Ruta de la imagen
                    alt="Divisor",
                    width="100%",  # Ancho de la imagen
                    height="50px",   # Altura ajustada automáticamente
                    
                ),
                rx.image(
                    src="/home-azure.png",  # Ruta de la imagen
                    alt="Descripción de la imagen",
                    width="100%",  # Ancho de la imagen
                    height="50vh",   # Altura ajustada automáticamente
                    
                ),
                rx.button(
                    "TEST NOW!",
                    style={
                        "position": "absolute",  # Coloca el botón encima de la imagen
                        "top": "95%",            # Posición vertical centrada
                        "left": "50%",           # Posición horizontal centrada
                        "transform": "translate(-50%, -50%)",  # Ajuste para centrar completamente
                        "background-color": "#9C0720",  # Fondo semi-transparente
                        "color": "white",
                        "padding": "30px 120px",
                        "font-size": "24px",     # Aumentar el tamaño de la fuente
                        "font-family": "'Roboto', sans-serif", 
                        "border": "3px solid #FFD700",
                        "border-radius": "5px",
                        "cursor": "pointer",
                        
                    },
                    _hover={
                        "color": "#FFD700"  # Cambia el color del texto al pasar el cursor
                    },
                    on_click=lambda: rx.redirect('/home/dashboard')
                    
                ),
                rx.image(
                    src="/divisor.png",  # Ruta de la imagen
                    alt="Divisor",
                    width="100%",  # Ancho de la imagen
                    height="50px",   # Altura ajustada automáticamente
                    
                ),
                
                
                direction="column",
                height="100%",
                background_color="#6495ED",
                width="80%",
            
            ),
            
            background_color="#bdbdbd",
            width="100%",
            height='100%'
            
        ),    
        
    height="fit-content",
    width="100%",
    )