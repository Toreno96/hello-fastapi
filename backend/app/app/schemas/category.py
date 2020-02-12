from typing import List

from pydantic import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    parent_id: int = None
    name: str = None


# Properties to receive on item creation
class CategoryCreate(CategoryBase):
    name: str


# Properties to receive on item update
class CategoryUpdate(CategoryBase):
    pass


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int
    parent_id: int = None
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass


class CategoryWithChildren(BaseModel):
    category: Category
    children: List[Category]


class CategoryNodeBase(BaseModel):
    id: int
    name: str
    children: List = None

    class Config:
        orm_mode = True


class CategoryNode(CategoryNodeBase):
    """This and CategoryNodeBase are workaround classes, because FastAPI have problems with self-referencing models:
    <https://pydantic-docs.helpmanual.io/usage/postponed_annotations/#self-referencing-models>

    It is not working:

    ```
    class CategoryNode(BaseModel):
        ...
        children: List['CategoryNode']

    CategoryNode.update_forward_refs()
    ```

    Nor use of `__future__.annotations`.

    There are errors during startup.
    """

    children: List[CategoryNodeBase] = None
