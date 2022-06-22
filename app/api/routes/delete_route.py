from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.schemas.output_schemas import Error

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
    При удалении категории удаляются все дочерние элементы.
    Доступ к статистике (истории обновлений) удаленного элемента невозможен.

    Так как время удаления не передается,
    при удалении элемента время обновления родителя изменять не нужно.

    **Обратите, пожалуйста, внимание на этот обработчик.
    При его некорректной работе тестирование может быть невозможно.**
    :param session:
    :param id:
    :return:
        "200":
          description: Вставка или обновление прошли успешно.
        "400":
          description: Невалидная схема документа или входные данные не верны.
          {
                "code": 400,
                "message": "Validation Failed"
          }
        "404":
          description: Категория/товар не найден.
          {
                "code": 404,
                "message": "Item not found"
          }
    """
