from sqlalchemy import Column, Integer, String
from sqlalchemy_mptt.mixins import BaseNestedSets

from app.db.base_class import Base


class BaseNestedSets(BaseNestedSets):
    @classmethod
    def _node_to_dict(cls, node, json, json_fields):
        """ Helper method for ``get_tree``.
        """
        if json:
            pk_name = node.get_pk_name()
            # jqTree or jsTree format
            result = {"id": getattr(node, pk_name)}
            if json_fields:
                result.update(json_fields(node))
        else:
            result = {"node": node}
        return result


class Category(Base, BaseNestedSets):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
