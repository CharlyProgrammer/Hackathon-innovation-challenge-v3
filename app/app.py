
import reflex as rx
from app.pages.home import home
from app.pages.dashboard import aplications_dashboard
from app.pages.about_project import about_project
from app.pages.about_team import about_team
from app.pages.image_analyzer import image_analyzer_page
from app.pages.web_pages_analyzer import web_analyzer_page


app = rx.App()
app.add_page(home, route="/home",title='Project Name - Home')
app.add_page(aplications_dashboard, route="/home/dashboard",title='Project name - Dashboard')
app.add_page(about_project, route="/home/about-project",title='Project name - about')
app.add_page(about_team, route="/home/about-team",title='Project name - our developers')
app.add_page(image_analyzer_page, route="/home/dashboard/image-analyzer",title='Project name - image analyzer')
app.add_page(web_analyzer_page, route="/home/dashboard/web-analyzer",title='Project name - Web analyzer')


