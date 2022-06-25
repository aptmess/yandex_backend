from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.core.models import Shop
from app.exceptions import (
    EXCEPTION_400_BAD_REQUEST_VALIDATION_ERROR,
    EXCEPTION_404_NOT_FOUND,
)
from app.schemas.error import Error
from app.schemas.response import HTTP_400_RESPONSE, HTTP_404_RESPONSE

router = APIRouter(route_class=LogRoute)


@router.delete(
    '/delete/{id}',
    response_model=None,
    responses={
        status.HTTP_200_OK: {
            'description': 'Вставка и обновление данных произошли успешно',
            'model': None,
        },
        status.HTTP_400_BAD_REQUEST: HTTP_400_RESPONSE,
        status.HTTP_404_NOT_FOUND: HTTP_404_RESPONSE,
    },
)
def delete_delete_id(
    id: UUID, session: Session = Depends(get_session)
) -> Union[None, Error]:
    """
    Удалить элемент по идентификатору.

    - При удалении категории удаляются все дочерние элементы.

    - Доступ к статистике (истории обновлений) удаленного элемента невозможен.

    - Так как время удаления не передается, при удалении элемента время обновления родителя изменять не нужно.

    **Обратите, пожалуйста, внимание на этот обработчик. При его некорректной работе тестирование может быть невозможно.**

    Output:

    - 200: Вставка или обновление прошли успешно.

    - 400: Невалидная схема документа или входные данные не верны. "Validation Failed"

    - 404: Категория/товар не найден. "Item not found"
    """
    shop = session.query(Shop).filter_by(id=id).one_or_none()
    if shop is None:
        raise EXCEPTION_404_NOT_FOUND
    try:
        session.delete(shop)
        session.commit()
        return Response(status_code=status.HTTP_200_OK)  # type: ignore
    except Exception as exc:
        raise EXCEPTION_400_BAD_REQUEST_VALIDATION_ERROR from exc
