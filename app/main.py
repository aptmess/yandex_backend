from fastapi import FastAPI

from app.api.routes import api
from app.config import config
from app.core.engine import engine, get_session
from app.core.models import Base


def get_application() -> FastAPI:
    application = FastAPI(
        title=config.SERVICE_NAME,
        description=config.DESCRIPTION,
        debug=config.DEBUG,
        version=config.VERSION,
        contact={
            'name': 'Aleksandr Shirokov',
            'email': 'improfeo@yandex.ru',
        },
    )

    @application.on_event('startup')
    async def startup() -> None:
        Base.metadata.create_all(engine)
        get_session()

    @application.on_event('shutdown')
    async def shutdown() -> None:
        pass

    application.include_router(api.full_api_router)

    return application


app = get_application()
