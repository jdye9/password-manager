from nicegui import ui


def page():
    ui.add_css('.nicegui-content { margin: 0; padding: 0; }')
    with ui.element('div').classes("flex w-[100vw] h-[100vh] bg-blue"):
        with ui.card().classes('flex mx-auto my-auto h-[200px] w-[400px]'):
            with ui.row().classes('mx-auto my-auto'):
                ui.label('🔐 PassHero').classes('text-3xl')
            with ui.column().classes('my-auto mx-auto'):
                with ui.row().classes('flex mx-auto'):
                    ui.button('Register', icon="account_circle", on_click=lambda: ui.navigate.to("/register")).props(
                        "push").classes('flex justify-start bg-blue w-[150px]')
                with ui.row().classes('flex mx-auto'):
                    ui.button('Log In', icon="lock_open").props(
                        "push").classes('justify-start bg-blue w-[150px]')
                with ui.row().classes('flex mx-auto'):
                    ui.button('Reset', icon="lock_reset").props(
                        "push").classes('justify-start bg-blue w-[150px]')
