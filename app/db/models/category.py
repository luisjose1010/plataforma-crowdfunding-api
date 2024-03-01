from sqlalchemy import Column, func, select, Integer, String, Float
from sqlalchemy.orm import relationship, column_property
from db import models

from ..database import Base


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description= Column(String)
    url = Column(String, nullable=False, unique=True, index=True)
    projects_count = column_property(
        # No entiendo esta query, pero obtiene la cantidad de proyectos de la categoria
        select(func.count(models.Project.category_id)).filter(models.Project.category_id == id).scalar_subquery(),
        deferred=True,
    )

    projects = relationship("Project", back_populates="category")