from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .usecases import ItemUsecase

from ..common import get_db

from .schema import CreateItemRequest, CreateItemResponse
from be_task_ca.interface import dependencies


item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(
    item: CreateItemRequest,
    items_usecase: ItemUsecase = Depends(dependencies.get_items_usecase),
) -> CreateItemResponse:
    return items_usecase.create_item(item)


@item_router.get("/")
async def get_items(
    items_usecase: ItemUsecase = Depends(dependencies.get_items_usecase),
):
    return items_usecase.get_all()
