from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser, get_current_active_user
from app.models.user import User as DBUser
from app.schemas.category import (
    Category,
    CategoryCreate,
    CategoryNode,
    CategoryUpdate,
    CategoryWithChildren,
)

router = APIRouter()


@router.get("/", response_model=List[Category])
def read_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Retrieve categories.
    """
    categories = crud.category.get_multi(db, skip=skip, limit=limit)
    return categories


@router.get("/tree/", response_model=List[CategoryNode])
def read_categories_tree(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Retrieve categories.
    """

    def fields(node):
        return {"name": node.name}

    categories = crud.category.model.get_tree(db, json=True, json_fields=fields)

    return categories


@router.get(
    "/{category_id}", response_model=Category,
)
def read_category_by_id(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    current_user: DBUser = Depends(get_current_active_user),
):
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404)
    return category


@router.get(
    "/{category_id}/children", response_model=CategoryWithChildren,
)
def read_category_children_by_id(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    current_user: DBUser = Depends(get_current_active_user),
):
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404)
    children = category.get_children(db)
    return CategoryWithChildren(category=category, children=children.all())


@router.get("/v2/{category_id}", response_model=Union[Category, CategoryWithChildren])
def read_category_id_v2(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    include_children: bool = False,
    current_user: DBUser = Depends(get_current_active_user),
):
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404)
    if include_children:
        children = category.get_children(db)
        return CategoryWithChildren(category=category, children=children.all())
    return category


@router.post("/", response_model=Category)
def create_category(
    *,
    db: Session = Depends(get_db),
    category_in: CategoryCreate,
    current_user: DBUser = Depends(get_current_active_superuser),
):
    """
    Create new category.
    """
    category = crud.category.create(db_session=db, obj_in=category_in)
    return category


@router.put("/{category_id}", response_model=Category)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    category_in: CategoryUpdate,
    current_user: DBUser = Depends(get_current_active_superuser),
):
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404)
    category = crud.category.update(db, db_obj=category, obj_in=category_in)
    return category
