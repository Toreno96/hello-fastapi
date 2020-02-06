from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.crud.base import CRUDBase


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_query_object(self, db_session: Session):
        return super().get_query_object(db_session).filter(self.model.is_deleted == False)

    def create_with_owner(
        self, db_session: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db_session: Session, *, owner_id: int, skip=0, limit=100
    ) -> List[Item]:
        return (
            self.get_query_object(db_session)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def remove(self, db_session: Session, *, id: int) -> Item:
        obj = self.get_query_object(db_session).filter(self.model.id == id).first()
        obj.is_deleted = True
        db_session.commit()
        return obj


item = CRUDItem(Item)
