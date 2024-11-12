from nicegui import app, ui
from ui.router import router
from data_classes.db import Database

if __name__ in {"__main__", "__mp_main__"}:
    app.include_router(router)
    app.native.window_args['resizable'] = False
    app.native.start_args['debug'] = True
    app.native.settings['ALLOW_DOWNLOADS'] = True
    db = Database("test.db")
    db.generate_tables()
    ui.run(title="PassHero", native=True,
           window_size=(1024, 768), fullscreen=False)
