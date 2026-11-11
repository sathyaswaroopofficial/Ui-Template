"""HTTP layer: parse request, call service, return schema."""

from fastapi import APIRouter, Depends, status

from app.modules.items.schemas import ItemCreate, ItemRead
from app.modules.items.service import ItemService, get_item_service

router = APIRouter()


@router.get("", response_model=list[ItemRead])
def list_items(service: ItemService = Depends(get_item_service)):
    return service.list_items()


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, service: ItemService = Depends(get_item_service)):
    return service.get_item(item_id)


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate, service: ItemService = Depends(get_item_service)):
    return service.create_item(data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    service.delete_item(item_id)
