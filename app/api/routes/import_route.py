from typing import Union

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.routes.log_route import LogRoute
from app.core.engine import get_session
from app.core.models import Shop, ShopHistory
from app.exceptions import EXCEPTION_400_BAD_REQUEST_VALIDATION_ERROR
from app.schemas.error import Error
from app.schemas.response import HTTP_400_RESPONSE
from app.schemas.shop_item import ShopUnitImportRequest

router = APIRouter(route_class=LogRoute)


@router.post(
    '/imports',
    response_model=None,
    responses={
        status.HTTP_200_OK: {
            'description': 'Вставка и обновление данных произошли успешно',
            'model': None,
        },
        status.HTTP_404_NOT_FOUND: HTTP_400_RESPONSE,
    },
)
def post_imports(  # type: ignore
    body: ShopUnitImportRequest = None, session: Session = Depends(get_session)  # type: ignore
) -> Union[None, Error]:  # type: ignore
    """
    Импортирует новые товары и/или категории.

    - Товары/категории импортированные повторно обновляют текущие.

    - Изменение типа элемента с товара на категорию или с категории на товар не допускается.

    - Порядок элементов в запросе является произвольным.

        - uuid товара или категории является уникальным среди товаров и категорий

        - родителем товара или категории может быть только категория

        - принадлежность к категории определяется полем parentId

        - товар или категория могут не иметь родителя (при обновлении parentId на null, элемент остается без родителя)

        - название элемента не может быть null

        - у категорий поле price должно содержать null

        - цена товара не может быть null и должна быть больше либо равна нулю.

        - при обновлении товара/категории обновленными считаются **все** их параметры

        - при обновлении параметров элемента обязательно обновляется поле **date** в соответствии с временем обновления

        - в одном запросе не может быть двух элементов с одинаковым id

        - дата должна обрабатываться согласно ISO 8601 (такой придерживается OpenAPI).

        - Если дата не удовлетворяет данному формату, необходимо отвечать 400.

    - Гарантируется, что во входных данных нет циклических зависимостей и поле updateDate монотонно возрастает.

    - Гарантируется, что при проверке передаваемое время кратно секундам.

    Output:

    - 200: Вставка или обновление прошли успешно.

    - 400: Невалидная схема документа или входные данные не верны. "Validation Failed"
    """
    if body is None:
        return Response(status_code=status.HTTP_200_OK)
    response = body.dict()
    updated_date = response['updateDate']
    if body is not None:
        for value in response['items']:
            shop = (
                session.query(Shop).filter(Shop.id == value['id']).one_or_none()
            )
            if shop is not None and shop.type != value['type']:
                raise EXCEPTION_400_BAD_REQUEST_VALIDATION_ERROR
            session.merge(Shop(**value))
            session.add(ShopHistory(**value, date=updated_date))

        session.commit()
    return Response(status_code=status.HTTP_200_OK)  # type: ignore
