from nicegui import ui


def page():
    ui.add_css('.nicegui-content { margin: 0; padding: 0; }')
    with ui.element('div').classes("flex w-[100vw] h-[100vh] bg-blue"):
        with ui.card().classes('flex mx-auto my-auto h-[200px] w-[400px]'):
            with ui.row().classes('mx-auto my-auto'):
                ui.label('🔐 PassHero').classes('text-3xl')
