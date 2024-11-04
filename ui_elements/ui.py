from nicegui import app, ui
from ui_elements.router import Router

@ui.page("/")  # normal index page (e.g. the entry point of the app)
@ui.page(
  "/{_:path}"
)  # all other pages will be handled by the router but must be registered to also show the SPA index page


class UI:

  def __init__(self) -> None:
    self._router = Router()
    self._router.add("/", self.home)
    self._router.add("/register", self.register)
    app.native.window_args['resizable'] = False
    app.native.start_args['debug'] = True
    app.native.settings['ALLOW_DOWNLOADS'] = True
    ui.add_css('.nicegui-content { margin: 0; padding: 0; }')
    lambda: self._router.open(self.home)
    self._router.frame()
    ui.run(title="PassHero", native=True, window_size=(1024, 768), fullscreen=False)

  def home(self):
    with ui.element('div').classes("flex w-[100vw] h-[100vh] bg-blue"):
      with ui.card().classes('flex mx-auto my-auto h-[200px] w-[400px]'):
        with ui.row().classes('mx-auto my-auto'):
          ui.label('🔐 PassHero').classes('text-3xl')
        with ui.column().classes('my-auto mx-auto'):
          with ui.row().classes('flex mx-auto'):
            ui.button('Register', icon="account_circle", on_click=lambda: self._router.open(self.register)).props("push").classes('flex justify-start bg-blue w-[150px]')
          with ui.row().classes('flex mx-auto'):
            ui.button('Log In', icon="lock_open").props("push").classes('justify-start bg-blue w-[150px]')
          with ui.row().classes('flex mx-auto'):
            ui.button('Reset', icon="lock_reset").props("push").classes('justify-start bg-blue w-[150px]')

  def register(self):
    with ui.element('div').classes("flex w-[100vw] h-[100vh] bg-blue"):
      with ui.row().classes('flex mx-auto'):
        ui.button('Back', icon="arrow_back", on_click=lambda: self._router.open(self.home)).props("push").classes('justify-start bg-blue w-[150px]')