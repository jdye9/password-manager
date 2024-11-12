from nicegui import APIRouter
from ui.pages.register.register import page as render_register
from ui.pages.landing import page as render_landing

router = APIRouter()


@router.page('/')
def landing():
    render_landing()


@router.page("/register")
def register():
    render_register()
