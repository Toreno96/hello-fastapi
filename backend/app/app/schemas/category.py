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
    """This and CategoryNodeBase are workaround classes, because it is not possible to do:

    ```
    class CategoryNode(BaseModel):
        ...
        children: List[CategoryNode]  # should be possible since Python 4.0: https://stackoverflow.com/a/33533514/5875021
    ```

    Nor `List['CategoryNode']`.

    There are errors during validation and docs generation.
    """

    children: List[CategoryNodeBase] = None
