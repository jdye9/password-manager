from nicegui import ui
from data_classes.credentials import Credentials
from data_classes.db import Database
from ui.pages.register.utils import check_validity, validate_input

db = Database("test.db")
credentials = Credentials()


def page():
    ui.add_css('.nicegui-content { margin: 0; padding: 0; }')
    with ui.element('div').classes("flex w-[100vw] h-[100vh] bg-blue"):
        with ui.card().classes('flex text-sm mx-auto my-auto w-[400px] pt-[50px] pb-[50px]'):
            with ui.column().classes('my-auto mx-auto'):
                ui.label('Register').classes(
                    'text-center text-3xl mx-auto mb-[20px]')
                with ui.row().classes('mx-auto my-auto'):
                    username = ui.input(label='Username', placeholder='start typing', on_change=lambda e: validate_input("username", e.value, username_icon)).classes(
                        "w-[250px]")
                    username_icon = ui.icon('person', color="blue").classes(
                        'text-2xl my-auto')
                with ui.row().classes('flex mx-auto my-auto'):
                    password = ui.input(label='Password', placeholder='start typing', on_change=lambda e: validate_input("password", e.value, password_icon)).classes(
                        "w-[250px]")
                    password_icon = ui.icon('lock', color="blue").classes(
                        'text-2xl my-auto')
                with ui.row().classes('flex mx-auto my-auto mt-[20px]'):
                    ui.button('Create Account', on_click=lambda: check_validity(username.value, password.value)).props(
                        "push").classes('flex justify-start bg-blue')
