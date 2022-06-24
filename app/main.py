from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                {'message': f'Validation Failed', 'error': exc.errors()}
            ),
        )

    application.include_router(api.full_api_router)

    return application


app = get_application()
