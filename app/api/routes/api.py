from fastapi import APIRouter

from app.api.routes import (
    delete_route,
    import_route,
    node_statistic_route,
    nodes_route,
    sales_route,
)

full_api_router = APIRouter()
full_api_router.include_router(delete_route.router, tags=['base_tasks'])
full_api_router.include_router(nodes_route.router, tags=['base_tasks'])
full_api_router.include_router(import_route.router, tags=['base_tasks'])
full_api_router.include_router(
    node_statistic_route.router, tags=['advanced_tasks']
)
full_api_router.include_router(sales_route.router, tags=['advanced_tasks'])
