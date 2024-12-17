
import reflex as rx
from app.pages.home import home
from app.pages.dashboard import aplications_dashboard





app = rx.App()
app.add_page(home, route="/home",title='Project Name - Home')
app.add_page(aplications_dashboard, route="/home/dashboard",title='Project name - Dashboard')
