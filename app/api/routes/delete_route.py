from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.core.models import Shop
from app.schemas.error import Error

router = APIRouter(route_class=LogRoute)


@router.delete(
    '/delete/{id}',
    response_model=None,
    responses={'400': {'model': Error}, '404': {'model': Error}},
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Item not found'
        )
    try:
        session.delete(shop)
        session.commit()
        return Response(status_code=status.HTTP_200_OK)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Validation Failed'
        )
