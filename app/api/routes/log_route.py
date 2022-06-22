from typing import Callable

from fastapi import Request, Response, exceptions
from fastapi.routing import APIRoute
from loguru import logger


class LogRoute(APIRoute):
    def get_route_handler(self) -> Callable:  # type: ignore
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            logger.info(f'{request.method} {request.url}')
            params_items = request.path_params.items()
            if params_items:
                logger.info(f'Params: {params_items}')

            headers_dict = dict(request.headers)
            if 'authorization' in headers_dict:
                headers_dict['authorization'] = 'hidden'

            logger.info(f'Headers: {headers_dict.items()}')

            body = await request.body()
            if body:
                logger.info(f'request body: {body.decode("utf-8")}')  # type: ignore

            try:
                response: Response = await original_route_handler(request)
            except exceptions.HTTPException as e:
                logger.error(f'{e.status_code}, {e.detail}')
                raise e

            logger.info(f'route response status_code={response.status_code}')
            if hasattr(response, 'body'):
                logger.info(
                    f'route response '
                    f'status_code={response.body.decode("utf-8")}'
                )  # type: ignore
            return response

        return custom_route_handler
