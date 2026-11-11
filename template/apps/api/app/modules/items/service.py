"""Business logic. Knows nothing about HTTP."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import NotFoundError
from app.modules.items.models import Item
from app.modules.items.repository import ItemRepository
from app.modules.items.schemas import ItemCreate


class ItemService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    def list_items(self) -> list[Item]:
        return self.repo.list()

    def get_item(self, item_id: int) -> Item:
        item = self.repo.get(item_id)
        if item is None:
            raise NotFoundError(f"Item {item_id} not found")
        return item

    def create_item(self, data: ItemCreate) -> Item:
        return self.repo.add(Item(name=data.name.strip(), description=data.description))

    def delete_item(self, item_id: int) -> None:
        self.repo.delete(self.get_item(item_id))


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(ItemRepository(db))
