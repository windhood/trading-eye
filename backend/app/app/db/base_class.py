from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func

@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
class TimestampMixin:
    """ Mixin to add update_at and created_at columns
    The columns are added at the *end* of the table
    """
    @declared_attr
    def updated_at(self):
        """ Last update timestamp """
        column = Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )
        # pylint: disable=protected-access
        column._creation_order = 9800
        return column

    @declared_attr
    def created_at(self):
        """ Creation timestamp """
        column = Column(
            DateTime(timezone=True),
            server_default=func.now()
        )
        # pylint: disable=protected-access
        column._creation_order = 9900
        return column
