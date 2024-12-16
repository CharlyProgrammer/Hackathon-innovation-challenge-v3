
import reflex as rx
from app.pages.home import home






app = rx.App()
app.add_page(home, route="/home",title='Sistema inteligente de autoevaluación de conocimientos')
